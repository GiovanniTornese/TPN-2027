"""End-of-shift reports: hours (0.5 steps, max 2), publications, admin-only comment."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from lib.auth import current_user, require_admin
from lib.db import db
from lib.shift_utils import has_ended, serialize
from models.schemas import AdminReportsOut, MyReportsOut, ReportIn, ReportOut, VolunteerTotals

router = APIRouter()


def full_name(u: dict | None) -> str:
    return f"{(u or {}).get('first_name', '')} {(u or {}).get('last_name', '')}".strip() or "Account eliminato"


async def to_out(reports: list[dict], with_comment: bool) -> list[ReportOut]:
    shifts = {s["id"]: s async for s in db.shifts.find({"id": {"$in": [r["shift_id"] for r in reports]}}, {"_id": 0})}
    users = {u["id"]: u async for u in db.users.find({"id": {"$in": [r["user_id"] for r in reports]}}, {"_id": 0})}
    out = []
    for r in reports:
        s = shifts.get(r["shift_id"], {})
        ts = r["updated_at"]
        out.append(ReportOut(
            id=r["id"], shift_id=r["shift_id"], user_id=r["user_id"], user_name=full_name(users.get(r["user_id"])),
            station=s.get("station", ""), date=s.get("date", ""), start=s.get("start", ""), end=s.get("end", ""),
            hours=r["hours"], publications=r["publications"],
            comment=r.get("comment", "") if with_comment else None,
            updated_at=ts.replace(tzinfo=timezone.utc) if ts.tzinfo is None else ts,
        ))
    return out


@router.put("/shifts/{shift_id}/report", response_model=ReportOut)
async def submit_report(shift_id: str, body: ReportIn, user: dict = Depends(current_user)):
    s = await db.shifts.find_one({"id": shift_id}, {"_id": 0})
    if not s:
        raise HTTPException(404, "Turno non trovato")
    if user["id"] not in s.get("volunteer_ids", []):
        raise HTTPException(403, "Puoi inserire il resoconto solo dei tuoi turni")
    if not has_ended(s):
        raise HTTPException(400, "Il resoconto si inserisce a fine turno")
    now = datetime.now(timezone.utc)
    await db.reports.update_one(
        {"shift_id": shift_id, "user_id": user["id"]},
        {"$set": {"hours": body.hours, "publications": body.publications, "comment": body.comment.strip(), "updated_at": now},
         "$setOnInsert": {"id": str(uuid.uuid4()), "shift_id": shift_id, "user_id": user["id"], "created_at": now}},
        upsert=True,
    )
    doc = await db.reports.find_one({"shift_id": shift_id, "user_id": user["id"]}, {"_id": 0})
    return (await to_out([doc], with_comment=True))[0]


@router.get("/reports/me", response_model=MyReportsOut)
async def my_reports(user: dict = Depends(current_user)):
    docs = await db.reports.find({"user_id": user["id"]}, {"_id": 0}).sort("updated_at", -1).to_list(1000)
    done = {d["shift_id"] for d in docs}
    mine = await db.shifts.find({"volunteer_ids": user["id"], "id": {"$nin": list(done)}}, {"_id": 0}) \
        .sort([("date", -1), ("start", -1)]).to_list(200)
    pending = [s for s in mine if has_ended(s)]
    return MyReportsOut(
        total_hours=sum(d["hours"] for d in docs), total_publications=sum(d["publications"] for d in docs),
        reports=await to_out(docs, with_comment=True), pending=await serialize(pending, user),
    )


@router.get("/reports", response_model=AdminReportsOut)
async def all_reports(month: Optional[str] = Query(default=None, pattern=r"^\d{4}-\d{2}$"), _: dict = Depends(require_admin)):
    docs = await db.reports.find({}, {"_id": 0}).sort("updated_at", -1).to_list(10000)
    out = await to_out(docs, with_comment=True)
    if month:
        out = [r for r in out if r.date.startswith(month)]
    totals: dict[str, VolunteerTotals] = {}
    for r in out:
        t = totals.setdefault(r.user_id, VolunteerTotals(user_id=r.user_id, user_name=r.user_name, hours=0, publications=0, reports=0))
        t.hours += r.hours
        t.publications += r.publications
        t.reports += 1
    return AdminReportsOut(
        total_hours=sum(r.hours for r in out), total_publications=sum(r.publications for r in out),
        total_reports=len(out), by_volunteer=sorted(totals.values(), key=lambda t: -t.hours), reports=out,
    )
