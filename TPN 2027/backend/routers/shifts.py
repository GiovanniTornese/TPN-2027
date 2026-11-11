import uuid
from datetime import date as Date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.errors import DuplicateKeyError

from lib.auth import current_user, require_admin
from lib.dates import today_iso
from lib.db import db
from lib.shift_utils import MAX_MEMBERS, MONTHLY_LIMIT, month_usage, place, remove_volunteer, serialize
from models.schemas import (
    DATE_PATTERN, AssignIn, JoinIn, MonthUsageOut, RemindersOut, ShiftBulkOut, ShiftCreateIn, ShiftIn, ShiftOut,
)

router = APIRouter()
DUP_MSG = "Esiste già un turno per questa postazione, data e orario"
MAX_REPEATS = 60


async def load(shift_id: str) -> dict:
    s = await db.shifts.find_one({"id": shift_id}, {"_id": 0})
    if not s:
        raise HTTPException(404, "Turno non trovato")
    return s


async def check_station(key: str) -> None:
    if not await db.stations.find_one({"key": key, "archived": {"$ne": True}}):
        raise HTTPException(400, "Postazione non valida")


@router.get("/shifts", response_model=list[ShiftOut])
async def list_shifts(
    start: str = Query(pattern=DATE_PATTERN),
    end: str = Query(pattern=DATE_PATTERN),
    station: Optional[str] = None,
    user: dict = Depends(current_user),
):
    q: dict = {"date": {"$gte": start, "$lte": end}}
    if station:
        q["station"] = station
    docs = await db.shifts.find(q, {"_id": 0}).sort([("date", 1), ("start", 1), ("station", 1)]).to_list(2000)
    return await serialize(docs, user)


@router.get("/shifts/my-usage", response_model=MonthUsageOut)
async def my_usage(month: str = Query(pattern=r"^\d{4}-\d{2}$"), user: dict = Depends(current_user)):
    return MonthUsageOut(month=month, used=await month_usage(user["id"], f"{month}-01"), limit=MONTHLY_LIMIT)


@router.get("/shifts/leading", response_model=list[ShiftOut])
async def my_leading_shifts(user: dict = Depends(current_user)):
    """Upcoming shifts where the caller is capoturno — includes the members' phone numbers."""
    docs = await db.shifts.find({"leader_id": user["id"], "date": {"$gte": today_iso()}}, {"_id": 0}) \
        .sort([("date", 1), ("start", 1)]).to_list(200)
    return await serialize(docs, user, show_phones=True)


@router.get("/shifts/uncovered", response_model=list[ShiftOut])
async def uncovered_shifts(user: dict = Depends(require_admin)):
    """Upcoming shifts still missing the capoturno or one of the two volunteers."""
    q = {
        "date": {"$gte": today_iso()},
        "$or": [{"leader_id": None}, {f"member_ids.{MAX_MEMBERS - 1}": {"$exists": False}}],
    }
    docs = await db.shifts.find(q, {"_id": 0}).sort([("date", 1), ("start", 1), ("station", 1)]).to_list(1000)
    return await serialize(docs, user)


@router.get("/me/reminders", response_model=RemindersOut)
async def my_reminders(user: dict = Depends(current_user)):
    """In-app reminder: the caller's shifts happening tomorrow."""
    tomorrow = (Date.fromisoformat(today_iso()) + timedelta(days=1)).isoformat()
    docs = await db.shifts.find({"volunteer_ids": user["id"], "date": tomorrow}, {"_id": 0}).sort("start", 1).to_list(20)
    return RemindersOut(tomorrow=tomorrow, shifts=await serialize(docs, user))


@router.post("/shifts", response_model=ShiftBulkOut)
async def create_shift(body: ShiftCreateIn, user: dict = Depends(require_admin)):
    await check_station(body.station)
    dates = [body.date]
    if body.repeat_until:
        if body.repeat_until < body.date:
            raise HTTPException(400, "La data di fine ripetizione deve essere successiva alla data del turno")
        d, until = Date.fromisoformat(body.date), Date.fromisoformat(body.repeat_until)
        while (d := d + timedelta(days=7)) <= until:
            dates.append(d.isoformat())
        if len(dates) > MAX_REPEATS:
            raise HTTPException(400, f"Massimo {MAX_REPEATS} turni ripetuti per volta")
    series_id = str(uuid.uuid4()) if len(dates) > 1 else None
    created, skipped = [], []
    for d in dates:
        doc = {
            "id": str(uuid.uuid4()), "station": body.station, "date": d, "start": body.start, "end": body.end,
            "leader_id": None, "member_ids": [], "volunteer_ids": [], "series_id": series_id,
        }
        try:
            await db.shifts.insert_one(doc)
            created.append(doc)
        except DuplicateKeyError:
            skipped.append(d)
    if not created:
        raise HTTPException(409, DUP_MSG)
    return ShiftBulkOut(created=await serialize(created, user), skipped_dates=skipped)


@router.put("/shifts/{shift_id}", response_model=ShiftOut)
async def update_shift(shift_id: str, body: ShiftIn, user: dict = Depends(require_admin)):
    s = await load(shift_id)
    if body.station != s["station"]:
        await check_station(body.station)
    data = {"station": body.station, "date": body.date, "start": body.start, "end": body.end}
    try:
        await db.shifts.update_one({"id": shift_id}, {"$set": data})
    except DuplicateKeyError:
        raise HTTPException(409, DUP_MSG)
    return (await serialize([{**s, **data}], user))[0]


@router.delete("/shifts/{shift_id}")
async def delete_shift(shift_id: str, _: dict = Depends(require_admin)):
    res = await db.shifts.delete_one({"id": shift_id})
    if not res.deleted_count:
        raise HTTPException(404, "Turno non trovato")
    await db.reports.delete_many({"shift_id": shift_id})
    return {"ok": True}


@router.post("/shifts/{shift_id}/join", response_model=ShiftOut)
async def join_shift(shift_id: str, body: Optional[JoinIn] = None, user: dict = Depends(current_user)):
    as_role = (body or JoinIn()).as_role
    if user["role"] != "volunteer":
        raise HTTPException(403, "Gli amministratori si assegnano dal pulsante Assegna")
    if user.get("gender") not in ("M", "F") or not user.get("phone"):
        raise HTTPException(400, "Completa il profilo (genere e telefono) prima di iscriverti")
    s = await load(shift_id)
    if s["date"] < today_iso():
        raise HTTPException(400, "Non è possibile iscriversi a un turno passato")
    await place(s, user, as_role, enforce_monthly=True)
    return (await serialize([await load(shift_id)], user))[0]


@router.post("/shifts/{shift_id}/assign", response_model=ShiftOut)
async def assign(shift_id: str, body: AssignIn, admin: dict = Depends(require_admin)):
    """Admin places any volunteer (or an admin, incl. themselves). Skips only the monthly limit."""
    s = await load(shift_id)
    target = await db.users.find_one({"id": body.user_id}, {"_id": 0})
    if not target:
        raise HTTPException(404, "Persona non trovata")
    await place(s, target, body.as_role, enforce_monthly=False)
    return (await serialize([await load(shift_id)], admin))[0]


@router.post("/shifts/{shift_id}/leave", response_model=ShiftOut)
async def leave_shift(shift_id: str, user: dict = Depends(current_user)):
    s = await load(shift_id)
    if user["id"] not in s.get("volunteer_ids", []):
        raise HTTPException(409, "Non sei iscritto a questo turno")
    if s["date"] < today_iso() and user["role"] != "admin":
        raise HTTPException(400, "Non è possibile cancellarsi da un turno passato")
    await remove_volunteer({"id": shift_id}, user["id"])
    return (await serialize([await load(shift_id)], user))[0]


@router.delete("/shifts/{shift_id}/volunteers/{user_id}", response_model=ShiftOut)
async def admin_remove(shift_id: str, user_id: str, admin: dict = Depends(require_admin)):
    await load(shift_id)
    if not await remove_volunteer({"id": shift_id}, user_id):
        raise HTTPException(404, "Volontario non iscritto a questo turno")
    return (await serialize([await load(shift_id)], admin))[0]
