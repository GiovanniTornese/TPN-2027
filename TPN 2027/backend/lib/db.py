"""Shared Mongo handle — import `client`/`db` from here (server.py, routers, seed.py)."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, IndexModel

load_dotenv(Path(__file__).parent.parent / ".env")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

logger = logging.getLogger(__name__)

# One entry per collection: every field a route filters, sorts, or dedupes on. Applied by ensure_indexes() at startup.
INDEXES: dict[str, list[IndexModel]] = {
    "users": [
        IndexModel([("id", ASCENDING)], name="id", unique=True),
        IndexModel([("email", ASCENDING)], name="email", unique=True),
        IndexModel([("role", ASCENDING), ("last_name", ASCENDING)], name="role_name"),
    ],
    "shifts": [
        IndexModel([("id", ASCENDING)], name="id", unique=True),
        IndexModel([("station", ASCENDING), ("date", ASCENDING), ("start", ASCENDING)], name="station_date_start", unique=True),
        IndexModel([("date", ASCENDING), ("start", ASCENDING)], name="date_start"),
        IndexModel([("volunteer_ids", ASCENDING), ("date", ASCENDING)], name="volunteer_date"),
        IndexModel([("leader_id", ASCENDING), ("date", ASCENDING)], name="leader_date"),
    ],
    "stations": [IndexModel([("key", ASCENDING)], name="key", unique=True)],
    "reports": [
        IndexModel([("id", ASCENDING)], name="id", unique=True),
        IndexModel([("shift_id", ASCENDING), ("user_id", ASCENDING)], name="shift_user", unique=True),
        IndexModel([("user_id", ASCENDING), ("updated_at", DESCENDING)], name="user_updated"),
    ],
    "reminders_sent": [IndexModel([("user_id", ASCENDING), ("date", ASCENDING)], name="user_date", unique=True)],
    "cron_runs": [
        IndexModel([("run_id", ASCENDING)], name="run_id", unique=True),
        IndexModel([("at", ASCENDING)], name="ttl", expireAfterSeconds=30 * 86400),
    ],
    "settings": [IndexModel([("key", ASCENDING)], name="key", unique=True)],
    "announcements": [
        IndexModel([("id", ASCENDING)], name="id", unique=True),
        IndexModel([("pinned", DESCENDING), ("created_at", DESCENDING)], name="pinned_created"),
    ],
}


async def ensure_indexes() -> None:
    for collection, models in INDEXES.items():
        for model in models:  # one at a time so a bad spec skips only itself
            try:
                await db[collection].create_indexes([model])
            except Exception as exc:  # never block boot on an index; the log line names what to fix
                logger.error("ensure_indexes(%s.%s): %s", collection, model.document["name"], exc)
