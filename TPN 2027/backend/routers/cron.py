"""Platform cron: day-before shift reminder emails (see .emergent/crons.yml)."""

import asyncio
import hmac
import logging
import os
from datetime import date as Date, datetime, timedelta, timezone
from html import escape

from fastapi import APIRouter, HTTPException, Request

from lib.dates import today_iso
from lib.db import db
from lib.email import send_email
from pymongo.errors import DuplicateKeyError

router = APIRouter()
logger = logging.getLogger(__name__)
_tasks: set[asyncio.Task] = set()


def _authorized(request: Request) -> bool:
    secret = os.environ.get("WEBHOOK_CRON_SECRET", "")
    header = request.headers.get("authorization", "")
    if not secret or not header.startswith("Bearer "):
        return False
    return hmac.compare_digest(header[7:].encode(), secret.encode())


def reminder_html(first_name: str, rows: list[tuple[str, str, str]], day_label: str) -> str:
    brand = escape(os.environ.get("EMAIL_FROM_NAME", "TPN 2027"))
    items = "".join(
        f'<tr><td style="padding:8px 0;border-bottom:1px solid #e2e8f0"><strong>{escape(t)}</strong> · {escape(st)}'
        f'<br><span style="color:#475569">Ruolo: {escape(role)}</span></td></tr>'
        for t, st, role in rows
    )
    return (
        '<table role="presentation" width="100%" style="background:#f8fafc"><tr><td style="padding:24px;font-family:Arial,sans-serif;color:#0f172a">'
        f'<h2 style="margin:0 0 12px">Promemoria turno di domani</h2>'
        f'<p>Ciao {escape(first_name)}, ti ricordiamo che <strong>{escape(day_label)}</strong> sei in turno:</p>'
        f'<table role="presentation" width="100%">{items}</table>'
        '<p>Se non puoi partecipare, cancella l\'iscrizione dall\'app il prima possibile così un altro volontario può prendere il tuo posto.</p>'
        f'<p style="font-size:12px;color:#64748b">Inviato da {brand} · Pianificazione turni.</p>'
        '</td></tr></table>'
    )


async def send_tomorrow_reminders() -> int:
    tomorrow = (Date.fromisoformat(today_iso()) + timedelta(days=1)).isoformat()
    shifts = await db.shifts.find({"date": tomorrow, "volunteer_ids.0": {"$exists": True}}, {"_id": 0}).to_list(2000)
    stations = {s["key"]: s["name"] async for s in db.stations.find({}, {"_id": 0})}
    per_user: dict[str, list[tuple[str, str, str]]] = {}
    for s in sorted(shifts, key=lambda x: x["start"]):
        for uid in s["volunteer_ids"]:
            role = "Capoturno" if s.get("leader_id") == uid else "Volontario"
            per_user.setdefault(uid, []).append((f"{s['start']}–{s['end']}", stations.get(s["station"], "Postazione"), role))
    day_label = datetime.fromisoformat(tomorrow).strftime("%d/%m/%Y")
    sent = 0
    async for u in db.users.find({"id": {"$in": list(per_user)}}, {"_id": 0}):
        try:  # one email per person per day, never twice
            await db.reminders_sent.insert_one({"user_id": u["id"], "date": tomorrow, "at": datetime.now(timezone.utc)})
        except DuplicateKeyError:
            continue
        if await send_email(to=u["email"], subject=f"Promemoria: domani sei in turno ({day_label})",
                            html=reminder_html(u.get("first_name", ""), per_user[u["id"]], day_label)):
            sent += 1
        else:
            await db.reminders_sent.delete_one({"user_id": u["id"], "date": tomorrow})
    logger.info(f"Reminder emails sent: {sent} for {tomorrow}")
    return sent


@router.post("/cron/reminders")
async def cron_reminders(request: Request):
    # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.
    if not _authorized(request):
        raise HTTPException(401, "Unauthorized")
    try:
        envelope = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid body")
    run_id = request.headers.get("x-webhook-id") or (envelope or {}).get("run_id") or ""
    if run_id:
        try:
            await db.cron_runs.insert_one({"run_id": run_id, "at": datetime.now(timezone.utc)})
        except DuplicateKeyError:
            return {"status": "duplicate"}
    task = asyncio.create_task(send_tomorrow_reminders())
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)
    return {"status": "accepted"}
