"""Idempotent startup seed: the two admin accounts (once), 3 stations, default 2h slots, shift-shape migration."""

import os
import uuid
from datetime import datetime, timezone

from lib.auth import hash_pw
from lib.db import db

DEFAULT_STATIONS = {"a": "Postazione A", "b": "Postazione B", "c": "Postazione C"}
DEFAULT_SLOTS = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]

# Seeded only once (settings flag), so later email/password changes made in-app are never overwritten.
ADMINS = [
    ("gnnitornese@gmail.com", "Giovanni", "Tornese"),
    ("andrea.volpicelli@tpn2027.it", "Andrea", "Volpicelli"),
]


async def bootstrap() -> None:
    if not await db.settings.find_one({"key": "admins_seeded_v2"}):
        await db.users.delete_many({"email": "admin@associazione.it", "role": "admin"})
        password = os.environ.get("ADMIN_PASSWORD", "Admin123!")
        for email, first, last in ADMINS:
            existing = await db.users.find_one({"email": email})
            if existing:
                await db.users.update_one({"email": email}, {"$set": {"role": "admin", "first_name": first, "last_name": last}})
                continue
            await db.users.insert_one({
                "id": str(uuid.uuid4()), "email": email, "password_hash": hash_pw(password),
                "role": "admin", "first_name": first, "last_name": last, "phone": "",
                "gender": "M", "is_team_leader": False, "created_at": datetime.now(timezone.utc),
            })
        await db.settings.insert_one({"key": "admins_seeded_v2"})

    if not await db.settings.find_one({"key": "stations_seeded"}):
        for i, (key, name) in enumerate(DEFAULT_STATIONS.items()):
            await db.stations.update_one({"key": key}, {"$setOnInsert": {"key": key, "name": name}}, upsert=True)
        await db.settings.insert_one({"key": "stations_seeded"})
    # Dynamic stations: make sure the original three have color/order/archived fields.
    for i, (key, color) in enumerate({"a": "emerald", "b": "indigo", "c": "amber"}.items()):
        await db.stations.update_one({"key": key, "color": {"$exists": False}},
                                     {"$set": {"color": color, "order": i, "archived": False}})
    await db.settings.update_one(
        {"key": "slots"}, {"$setOnInsert": {"key": "slots", "slots": DEFAULT_SLOTS}}, upsert=True
    )
    # Migrate shifts from the old men/women shape to leader + members.
    async for s in db.shifts.find({"member_ids": {"$exists": False}}):
        ids = s.get("volunteer_ids", [])[:2]
        await db.shifts.update_one(
            {"_id": s["_id"]},
            {"$set": {"leader_id": None, "member_ids": ids, "volunteer_ids": ids}, "$unset": {"men": "", "women": ""}},
        )
