import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from lib.auth import current_user, require_admin
from lib.db import db
from models.schemas import Announcement, AnnouncementIn

router = APIRouter()


def to_out(d: dict) -> Announcement:
    ts = d["created_at"]
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return Announcement(**{**d, "created_at": ts})


@router.get("/announcements", response_model=list[Announcement])
async def list_announcements(_: dict = Depends(current_user)):
    docs = await db.announcements.find({}, {"_id": 0}).sort([("pinned", -1), ("created_at", -1)]).to_list(500)
    return [to_out(d) for d in docs]


@router.post("/announcements", response_model=Announcement)
async def create_announcement(body: AnnouncementIn, admin: dict = Depends(require_admin)):
    author = f"{admin.get('first_name', '')} {admin.get('last_name', '')}".strip() or "Amministratore"
    doc = {"id": str(uuid.uuid4()), "title": body.title.strip(), "body": body.body.strip(),
           "pinned": body.pinned, "author_name": author, "created_at": datetime.now(timezone.utc)}
    await db.announcements.insert_one(doc)
    return to_out(doc)


@router.delete("/announcements/{aid}")
async def delete_announcement(aid: str, _: dict = Depends(require_admin)):
    res = await db.announcements.delete_one({"id": aid})
    if not res.deleted_count:
        raise HTTPException(404, "Avviso non trovato")
    return {"ok": True}
