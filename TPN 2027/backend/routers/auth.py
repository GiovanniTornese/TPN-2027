import uuid
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response

from lib.auth import clear_session, current_user, hash_pw, set_session, verify_pw
from lib.dates import today_iso
from lib.db import db
from models.schemas import CredentialsIn, GoogleSessionIn, LoginIn, ProfileIn, RegisterIn, UserPublic

router = APIRouter()
EMERGENT_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"


def public(user: dict) -> UserPublic:
    return UserPublic.model_validate({**user, "has_password": bool(user.get("password_hash"))})


async def has_upcoming_shifts(uid: str) -> bool:
    return bool(await db.shifts.find_one({"volunteer_ids": uid, "date": {"$gte": today_iso()}}))


async def check_gender_change(user: dict, new_gender: str) -> None:
    if user.get("gender") and user["gender"] != new_gender and await has_upcoming_shifts(user["id"]):
        raise HTTPException(400, "Impossibile cambiare genere con iscrizioni a turni futuri: annullale prima.")


def new_volunteer_doc(body: RegisterIn, is_team_leader: bool = False) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "email": body.email.lower(),
        "password_hash": hash_pw(body.password),
        "role": "volunteer",
        "first_name": body.first_name.strip(),
        "last_name": body.last_name.strip(),
        "phone": body.phone.strip(),
        "gender": body.gender,
        "is_team_leader": is_team_leader and body.gender == "M",
        "created_at": datetime.now(timezone.utc),
    }


@router.post("/auth/register", response_model=UserPublic)
async def register(body: RegisterIn, response: Response):
    if await db.users.find_one({"email": body.email.lower()}):
        raise HTTPException(409, "Email già registrata")
    doc = new_volunteer_doc(body)
    await db.users.insert_one(doc)
    set_session(response, doc["id"])
    return public(doc)


@router.post("/auth/login", response_model=UserPublic)
async def login(body: LoginIn, response: Response):
    user = await db.users.find_one({"email": body.email.lower()}, {"_id": 0})
    if not user or not verify_pw(body.password, user.get("password_hash", "")):
        raise HTTPException(401, "Email o password non corretti")
    set_session(response, user["id"])
    return public(user)


@router.post("/auth/google", response_model=UserPublic)
async def google_login(body: GoogleSessionIn, response: Response):
    """Exchange Emergent Google-auth session_id for our own cookie session (find-or-create by email)."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(EMERGENT_SESSION_URL, headers={"X-Session-ID": body.session_id})
    if r.status_code != 200:
        raise HTTPException(401, "Accesso con Google non riuscito")
    data = r.json()
    email = (data.get("email") or "").lower()
    if not email:
        raise HTTPException(401, "Accesso con Google non riuscito")
    user = await db.users.find_one({"email": email}, {"_id": 0})
    if not user:
        parts = (data.get("name") or "").strip().split(" ", 1)
        user = {
            "id": str(uuid.uuid4()), "email": email, "password_hash": "", "role": "volunteer",
            "first_name": parts[0] if parts else "", "last_name": parts[1] if len(parts) > 1 else "",
            "phone": "", "gender": None, "is_team_leader": False,
            "created_at": datetime.now(timezone.utc),
        }
        await db.users.insert_one(dict(user))
    set_session(response, user["id"])
    return public(user)


@router.post("/auth/logout")
async def logout(response: Response):
    clear_session(response)
    return {"ok": True}


@router.get("/auth/me", response_model=UserPublic)
async def me(user: dict = Depends(current_user)):
    return public(user)


@router.put("/me", response_model=UserPublic)
async def update_profile(body: ProfileIn, user: dict = Depends(current_user)):
    await check_gender_change(user, body.gender)
    data: dict = {k: (v.strip() if isinstance(v, str) else v) for k, v in body.model_dump().items()}
    if body.gender == "F":
        data["is_team_leader"] = False
    await db.users.update_one({"id": user["id"]}, {"$set": data})
    return public({**user, **data})


@router.put("/me/credentials", response_model=UserPublic)
async def update_credentials(body: CredentialsIn, user: dict = Depends(current_user)):
    if user.get("password_hash") and not verify_pw(body.current_password, user["password_hash"]):
        raise HTTPException(400, "Password attuale non corretta")
    email = body.email.lower()
    data: dict = {"email": email}
    if email != user["email"] and await db.users.find_one({"email": email}):
        raise HTTPException(409, "Email già in uso da un altro account")
    if body.new_password:
        data["password_hash"] = hash_pw(body.new_password)
    await db.users.update_one({"id": user["id"]}, {"$set": data})
    return public({**user, **data})
