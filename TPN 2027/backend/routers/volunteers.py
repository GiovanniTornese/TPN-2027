from fastapi import APIRouter, Depends, HTTPException

from lib.auth import hash_pw, require_admin
from lib.dates import today_iso
from lib.db import db
from lib.shift_utils import remove_volunteer
from models.schemas import VolunteerAdminIn, VolunteerCreateIn, VolunteerOut
from routers.auth import check_gender_change, new_volunteer_doc

router = APIRouter()


async def counts(field_filter: dict) -> dict[str, int]:
    pipeline = [{"$match": field_filter}, {"$unwind": "$volunteer_ids"},
                {"$group": {"_id": "$volunteer_ids", "n": {"$sum": 1}}}]
    return {d["_id"]: d["n"] async for d in db.shifts.aggregate(pipeline)}


def out(u: dict, **extra) -> VolunteerOut:
    return VolunteerOut.model_validate({**u, "has_password": bool(u.get("password_hash")), **extra})


@router.get("/volunteers", response_model=list[VolunteerOut])
async def list_volunteers(include_admins: bool = False, _: dict = Depends(require_admin)):
    roles = ["volunteer", "admin"] if include_admins else ["volunteer"]
    users = await db.users.find({"role": {"$in": roles}}, {"_id": 0}) \
        .sort([("last_name", 1), ("first_name", 1)]).to_list(5000)
    total = await counts({})
    upcoming = await counts({"date": {"$gte": today_iso()}})
    return [out(u, shift_count=total.get(u["id"], 0), upcoming_count=upcoming.get(u["id"], 0)) for u in users]


@router.post("/volunteers", response_model=VolunteerOut)
async def create_volunteer(body: VolunteerCreateIn, _: dict = Depends(require_admin)):
    if await db.users.find_one({"email": body.email.lower()}):
        raise HTTPException(409, "Email già registrata")
    doc = new_volunteer_doc(body, body.is_team_leader)
    await db.users.insert_one(doc)
    return out(doc)


async def load_volunteer(uid: str) -> dict:
    u = await db.users.find_one({"id": uid, "role": "volunteer"}, {"_id": 0})
    if not u:
        raise HTTPException(404, "Volontario non trovato")
    return u


@router.put("/volunteers/{uid}", response_model=VolunteerOut)
async def update_volunteer(uid: str, body: VolunteerAdminIn, _: dict = Depends(require_admin)):
    u = await load_volunteer(uid)
    await check_gender_change(u, body.gender)
    if body.is_team_leader and body.gender != "M":
        raise HTTPException(400, "Il capoturno deve essere un uomo")
    if not body.is_team_leader and u.get("is_team_leader") and await db.shifts.find_one(
        {"leader_id": uid, "date": {"$gte": today_iso()}}
    ):
        raise HTTPException(400, "È capoturno in turni futuri: rimuovilo prima da quei turni")
    data = {k: (v.strip() if isinstance(v, str) else v) for k, v in body.model_dump(exclude={"email", "new_password"}).items()}
    if body.email and body.email.lower() != u["email"]:
        if await db.users.find_one({"email": body.email.lower()}):
            raise HTTPException(409, "Email già in uso da un altro account")
        data["email"] = body.email.lower()
    if body.new_password:
        data["password_hash"] = hash_pw(body.new_password)
    await db.users.update_one({"id": uid}, {"$set": data})
    return out({**u, **data})


@router.delete("/volunteers/{uid}")
async def delete_volunteer(uid: str, _: dict = Depends(require_admin)):
    await load_volunteer(uid)
    await remove_volunteer({}, uid)
    await db.users.delete_one({"id": uid})  # reports are kept so association totals don't change
    return {"ok": True}
