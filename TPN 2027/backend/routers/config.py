import uuid

from fastapi import APIRouter, Depends, HTTPException

from lib.auth import current_user, require_admin
from lib.dates import today_iso
from lib.db import db
from models.schemas import SlotsIn, SlotsOut, Station, StationIn, TodayOut

router = APIRouter()
PALETTE = ["emerald", "indigo", "amber", "rose", "cyan", "violet", "lime", "orange", "fuchsia", "teal"]


@router.get("/today", response_model=TodayOut)
async def today():
    return TodayOut(today=today_iso())


@router.get("/stations", response_model=list[Station])
async def list_stations(_: dict = Depends(current_user)):
    """Active and archived stations (archived ones are kept so past shifts still show their name)."""
    docs = await db.stations.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    return [Station(**d) for d in docs]


@router.post("/stations", response_model=Station)
async def create_station(body: StationIn, _: dict = Depends(require_admin)):
    active = await db.stations.find({"archived": {"$ne": True}}, {"_id": 0}).to_list(100)
    used = {s.get("color") for s in active}
    color = next((c for c in PALETTE if c not in used), PALETTE[len(active) % len(PALETTE)])
    count = await db.stations.count_documents({})
    doc = {"key": uuid.uuid4().hex[:8], "name": body.name.strip(), "color": color, "archived": False, "order": count}
    await db.stations.insert_one(doc)
    return Station(**doc)


@router.put("/stations/{key}", response_model=Station)
async def rename_station(key: str, body: StationIn, _: dict = Depends(require_admin)):
    name = body.name.strip()
    if not name:
        raise HTTPException(422, "Nome obbligatorio")
    res = await db.stations.find_one_and_update({"key": key}, {"$set": {"name": name}}, projection={"_id": 0})
    if not res:
        raise HTTPException(404, "Postazione non trovata")
    return Station(**{**res, "name": name})


@router.delete("/stations/{key}")
async def delete_station(key: str, _: dict = Depends(require_admin)):
    if not await db.stations.find_one({"key": key, "archived": {"$ne": True}}):
        raise HTTPException(404, "Postazione non trovata")
    future = await db.shifts.count_documents({"station": key, "date": {"$gte": today_iso()}})
    if future:
        raise HTTPException(409, f"La postazione ha ancora {future} turni futuri: spostali o eliminali prima")
    if await db.stations.count_documents({"archived": {"$ne": True}}) <= 1:
        raise HTTPException(400, "Deve restare almeno una postazione")
    await db.stations.update_one({"key": key}, {"$set": {"archived": True}})
    return {"ok": True}


@router.get("/settings/slots", response_model=SlotsOut)
async def get_slots(_: dict = Depends(current_user)):
    doc = await db.settings.find_one({"key": "slots"}, {"_id": 0}) or {"slots": []}
    return SlotsOut(slots=doc["slots"])


@router.put("/settings/slots", response_model=SlotsOut)
async def set_slots(body: SlotsIn, _: dict = Depends(require_admin)):
    await db.settings.update_one({"key": "slots"}, {"$set": {"slots": body.slots}}, upsert=True)
    return SlotsOut(slots=body.slots)
