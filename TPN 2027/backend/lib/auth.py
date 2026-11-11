"""Cookie-session auth: JWT in an httpOnly cookie, user + role re-read from Mongo on every request."""

import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request, Response
from passlib.hash import pbkdf2_sha256

from lib.db import db

COOKIE = "session"
MAX_AGE = 7 * 24 * 3600
SECRET = os.environ["JWT_SECRET"]


def hash_pw(pw: str) -> str:
    return pbkdf2_sha256.hash(pw)


def verify_pw(pw: str, hashed: str) -> bool:
    try:
        return pbkdf2_sha256.verify(pw, hashed)
    except Exception:
        return False


def set_session(response: Response, user_id: str) -> None:
    exp = datetime.now(timezone.utc) + timedelta(seconds=MAX_AGE)
    token = jwt.encode({"sub": user_id, "exp": exp}, SECRET, algorithm="HS256")
    response.set_cookie(COOKIE, token, httponly=True, samesite="lax", max_age=MAX_AGE, path="/")


def clear_session(response: Response) -> None:
    response.delete_cookie(COOKIE, path="/")


async def current_user(request: Request) -> dict:
    token = request.cookies.get(COOKIE)
    if not token:
        raise HTTPException(401, "Non autenticato")
    try:
        sub = jwt.decode(token, SECRET, algorithms=["HS256"])["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Sessione non valida")
    user = await db.users.find_one({"id": sub}, {"_id": 0})
    if not user:
        raise HTTPException(401, "Utente non trovato")
    return user


async def require_admin(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Riservato agli amministratori")
    return user
