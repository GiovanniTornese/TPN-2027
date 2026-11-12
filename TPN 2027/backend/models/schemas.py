"""Pydantic models — every one mirrored by a TS interface in frontend/src/lib/types.ts."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

Gender = Literal["M", "F"]
Role = Literal["admin", "volunteer"]
ShiftRole = Literal["leader", "member"]

DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
HM_PATTERN = r"^([01]\d|2[0-3]):[0-5]\d$"
SLOT_PATTERN = r"^([01]\d|2[0-1]):[0-5]\d$"  # quick-pick 2h presets: last start 21:59


# ---------- users ----------
class UserPublic(BaseModel):
    id: str
    email: str
    role: Role
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    gender: Optional[Gender] = None
    is_team_leader: bool = False
    has_password: bool = False


class ProfileIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=60)
    last_name: str = Field(min_length=1, max_length=60)
    phone: str = Field(min_length=5, max_length=30)
    gender: Gender


class RegisterIn(ProfileIn):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class VolunteerAdminIn(ProfileIn):
    is_team_leader: bool = False
    email: Optional[EmailStr] = None
    new_password: Optional[str] = Field(default=None, min_length=6, max_length=128)


class VolunteerCreateIn(RegisterIn):
    is_team_leader: bool = False


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class GoogleSessionIn(BaseModel):
    session_id: str = Field(min_length=1)


class CredentialsIn(BaseModel):
    email: EmailStr
    current_password: str = ""
    new_password: Optional[str] = Field(default=None, min_length=6, max_length=128)


class VolunteerOut(UserPublic):
    shift_count: int = 0
    upcoming_count: int = 0


# ---------- config ----------
class Station(BaseModel):
    key: str
    name: str
    color: str = "emerald"
    archived: bool = False


class StationIn(BaseModel):
    name: str = Field(min_length=1, max_length=40)


class SlotsOut(BaseModel):
    slots: list[str]


class SlotsIn(BaseModel):
    slots: list[str] = Field(min_length=1, max_length=16)

    @field_validator("slots")
    @classmethod
    def check_slots(cls, v: list[str]) -> list[str]:
        import re

        for s in v:
            if not re.match(SLOT_PATTERN, s):
                raise ValueError(f"Orario non valido: {s} (formato HH:MM, max 21:00)")
        return sorted(set(v))


class TodayOut(BaseModel):
    today: str


# ---------- shifts ----------
class ShiftIn(BaseModel):
    station: str = Field(min_length=1)
    date: str = Field(pattern=DATE_PATTERN)
    start: str = Field(pattern=HM_PATTERN)
    end: str = Field(pattern=HM_PATTERN)

    @model_validator(mode="after")
    def check_range(self):
        if self.end <= self.start:
            raise ValueError("L'orario di fine deve essere successivo all'inizio")
        return self


class ShiftCreateIn(ShiftIn):
    repeat_until: Optional[str] = Field(default=None, pattern=DATE_PATTERN)


class JoinIn(BaseModel):
    as_role: ShiftRole = "member"


class AssignIn(BaseModel):
    user_id: str
    as_role: ShiftRole = "member"


class ShiftVolunteer(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: Optional[Gender] = None
    phone: Optional[str] = None  # admin only


class ShiftOut(BaseModel):
    id: str
    station: str
    date: str
    start: str
    end: str
    leader: Optional[ShiftVolunteer] = None
    members: list[ShiftVolunteer]
    missing_leader: bool
    free_member_slots: int
    free_slots: int
    is_complete: bool
    is_mine: bool
    my_role: Optional[ShiftRole] = None
    has_ended: bool = False
    my_report_done: bool = False


class ShiftBulkOut(BaseModel):
    created: list[ShiftOut]
    skipped_dates: list[str]


class MonthUsageOut(BaseModel):
    month: str
    used: int
    limit: int


# ---------- reports (resoconto fine turno) ----------
class ReportIn(BaseModel):
    hours: float = Field(ge=0.5, le=2)
    publications: int = Field(ge=0, le=10000)
    comment: str = Field(default="", max_length=2000)

    @field_validator("hours")
    @classmethod
    def half_steps(cls, v: float) -> float:
        if round(v * 2) != v * 2:
            raise ValueError("Le ore vanno indicate a mezz'ore (0,5 – 1 – 1,5 – 2)")
        return v


class ReportOut(BaseModel):
    id: str
    shift_id: str
    user_id: str
    user_name: str
    station: str
    date: str
    start: str
    end: str
    hours: float
    publications: int
    comment: Optional[str] = None  # admin + author only
    updated_at: datetime


class MyReportsOut(BaseModel):
    total_hours: float
    total_publications: int
    reports: list[ReportOut]
    pending: list[ShiftOut]


class VolunteerTotals(BaseModel):
    user_id: str
    user_name: str
    hours: float
    publications: int
    reports: int


class AdminReportsOut(BaseModel):
    total_hours: float
    total_publications: int
    total_reports: int
    by_volunteer: list[VolunteerTotals]
    reports: list[ReportOut]


class RemindersOut(BaseModel):
    tomorrow: str
    shifts: list[ShiftOut]


# ---------- announcements ----------
class AnnouncementIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(min_length=1, max_length=4000)
    pinned: bool = False


class Announcement(BaseModel):
    id: str
    title: str
    body: str
    pinned: bool
    author_name: str
    created_at: datetime
    # PULITO
