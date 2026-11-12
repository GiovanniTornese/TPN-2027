"""Shift helpers: time math, serialization, safe removal of a volunteer.

Shape: leader_id (capoturno) + member_ids (max 2, any gender).
volunteer_ids = leader + members, kept in sync for overlap / monthly-limit queries.
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from lib.db import db
from models.schemas import ShiftOut, ShiftVolunteer

MAX_MEMBERS = 2
MONTHLY_LIMIT = 2


def now_local() -> tuple[str, str]:
    """(YYYY-MM-DD, HH:MM) in APP_TZ."""
    n = datetime.now(ZoneInfo(os.environ.get("APP_TZ", "UTC")))
    return n.strftime("%Y-%m-%d"), n.strftime("%H:%M")


def has_ended(s: dict) -> bool:
    d, t = now_local()
    return s["date"] < d or (s["date"] == d and s["end"] <= t)


def end_plus_two(start: str) -> str:
    h, m = map(int, start.split(":"))
    return f"{h + 2:02d}:{m:02d}"


def can_lead(u: dict) -> bool:
    """Capoturno: a man enabled by an admin. Admins (men) can always lead."""
    return u.get("gender") == "M" and (u.get("is_team_leader") or u.get("role") == "admin")


async def serialize(shifts: list[dict], user: dict, show_phones: bool = False) -> list[ShiftOut]:
    ids = list({uid for s in shifts for uid in s.get("volunteer_ids", [])})
    users = {
        u["id"]: u
        async for u in db.users.find({"id": {"$in": ids}}, {"_id": 0, "password_hash": 0})
    }
    reported = {
        r["shift_id"]
        async for r in db.reports.find(
            {"user_id": user["id"], "shift_id": {"$in": [s["id"] for s in shifts]}}, {"shift_id": 1}
        )
    }
    phones = user["role"] == "admin" or show_phones

    def vol(uid: str | None) -> ShiftVolunteer | None:
        u = users.get(uid) if uid else None
        if not u:
            return None
        return ShiftVolunteer(
            id=uid, first_name=u.get("first_name", ""), last_name=u.get("last_name", ""),
            gender=u.get("gender"), phone=u.get("phone") if phones else None,
        )

    out: list[ShiftOut] = []
    for s in shifts:
        leader = vol(s.get("leader_id"))
        members = [v for uid in s.get("member_ids", []) if (v := vol(uid))]
        free_members = max(0, MAX_MEMBERS - len(s.get("member_ids", [])))
        missing_leader = not s.get("leader_id")
        my_role = "leader" if s.get("leader_id") == user["id"] else ("member" if user["id"] in s.get("member_ids", []) else None)
        out.append(ShiftOut(
            id=s["id"], station=s["station"], date=s["date"], start=s["start"], end=s["end"],
            leader=leader, members=members, missing_leader=missing_leader,
            free_member_slots=free_members, free_slots=free_members + (1 if missing_leader else 0),
            is_complete=not missing_leader and free_members == 0,
            is_mine=my_role is not None, my_role=my_role,
            has_ended=has_ended(s), my_report_done=s["id"] in reported,
        ))
    return out


async def remove_volunteer(shift_filter: dict, uid: str) -> int:
    """Remove uid from matching shifts (as leader or member). Returns modified count."""
    res = await db.shifts.update_many(
        {**shift_filter, "member_ids": uid}, {"$pull": {"member_ids": uid, "volunteer_ids": uid}}
    )
    res2 = await db.shifts.update_many(
        {**shift_filter, "leader_id": uid}, {"$set": {"leader_id": None}, "$pull": {"volunteer_ids": uid}}
    )
    return res.modified_count + res2.modified_count


async def month_usage(uid: str, date: str) -> int:
    return await db.shifts.count_documents({"volunteer_ids": uid, "date": {"$regex": f"^{date[:7]}-"}})


async def place(s: dict, target: dict, as_role: str, *, enforce_monthly: bool) -> None:
    """Atomically put `target` into shift `s` in `as_role`, enforcing seat, capoturno, overlap (and monthly) rules."""
    uid = target["id"]
    if uid in s.get("volunteer_ids", []):
        raise HTTPException(409, "Già iscritto a questo turno")
    if enforce_monthly and await month_usage(uid, s["date"]) >= MONTHLY_LIMIT:
        raise HTTPException(409, f"Hai già raggiunto il limite di {MONTHLY_LIMIT} turni per questo mese")
    overlap = await db.shifts.find_one({
        "date": s["date"], "volunteer_ids": uid, "id": {"$ne": s["id"]},
        "start": {"$lt": s["end"]}, "end": {"$gt": s["start"]},
    })
    if overlap:
        raise HTTPException(409, f"Già iscritto a un turno sovrapposto ({overlap['start']}-{overlap['end']})")
    if as_role == "leader":
        if not can_lead(target):
            raise HTTPException(403, "Solo gli uomini abilitati come capoturno possono ricoprire questo ruolo")
        res = await db.shifts.update_one(
            {"id": s["id"], "leader_id": None, "volunteer_ids": {"$ne": uid}},
            {"$set": {"leader_id": uid}, "$push": {"volunteer_ids": uid}},
        )
        if not res.modified_count:
            raise HTTPException(409, "Il posto di capoturno è già occupato")
    else:
        res = await db.shifts.update_one(
            {"id": s["id"], f"member_ids.{MAX_MEMBERS - 1}": {"$exists": False}, "volunteer_ids": {"$ne": uid}},
            {"$push": {"member_ids": uid, "volunteer_ids": uid}},
        )
        if not res.modified_count:
            raise HTTPException(409, "Posti volontario esauriti: resta libero solo il posto di capoturno")
