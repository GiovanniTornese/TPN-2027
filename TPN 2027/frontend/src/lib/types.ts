// Hand-written mirrors of backend/models/schemas.py — keep in sync.
export type Gender = "M" | "F";
export type Role = "admin" | "volunteer";
export type StationKey = string;

export interface UserPublic {
  id: string;
  email: string;
  role: Role;
  first_name: string;
  last_name: string;
  phone: string;
  gender: Gender | null;
  is_team_leader: boolean;
  has_password: boolean;
}

export interface ProfileIn {
  first_name: string;
  last_name: string;
  phone: string;
  gender: Gender;
}

export interface RegisterIn extends ProfileIn {
  email: string;
  password: string;
}

export interface VolunteerAdminIn extends ProfileIn {
  is_team_leader: boolean;
  email: string | null;
  new_password: string | null;
}

export interface VolunteerCreateIn extends RegisterIn {
  is_team_leader: boolean;
}

export interface GoogleSessionIn {
  session_id: string;
}

export interface CredentialsIn {
  email: string;
  current_password: string;
  new_password: string | null;
}

export type ShiftRole = "leader" | "member";

export interface JoinIn {
  as_role: ShiftRole;
}

export interface MonthUsageOut {
  month: string;
  used: number;
  limit: number;
}

export interface LoginIn {
  email: string;
  password: string;
}

export interface VolunteerOut extends UserPublic {
  shift_count: number;
  upcoming_count: number;
}

export interface Station {
  key: StationKey;
  name: string;
  color: string;
  archived: boolean;
}

export interface StationIn {
  name: string;
}

export interface SlotsOut {
  slots: string[];
}

export interface TodayOut {
  today: string;
}

export interface ShiftIn {
  station: StationKey;
  date: string;
  start: string;
  end: string;
}

export interface ShiftCreateIn extends ShiftIn {
  repeat_until: string | null;
}

export interface AssignIn {
  user_id: string;
  as_role: ShiftRole;
}

export interface ShiftVolunteer {
  id: string;
  first_name: string;
  last_name: string;
  gender: Gender | null;
  phone: string | null;
}

export interface ShiftOut {
  id: string;
  station: StationKey;
  date: string;
  start: string;
  end: string;
  leader: ShiftVolunteer | null;
  members: ShiftVolunteer[];
  missing_leader: boolean;
  free_member_slots: number;
  free_slots: number;
  is_complete: boolean;
  is_mine: boolean;
  my_role: ShiftRole | null;
  has_ended: boolean;
  my_report_done: boolean;
}

export interface ShiftBulkOut {
  created: ShiftOut[];
  skipped_dates: string[];
}

export interface ReportIn {
  hours: number;
  publications: number;
  comment: string;
}

export interface ReportOut {
  id: string;
  shift_id: string;
  user_id: string;
  user_name: string;
  station: string;
  date: string;
  start: string;
  end: string;
  hours: number;
  publications: number;
  comment: string | null;
  updated_at: string;
}

export interface MyReportsOut {
  total_hours: number;
  total_publications: number;
  reports: ReportOut[];
  pending: ShiftOut[];
}

export interface VolunteerTotals {
  user_id: string;
  user_name: string;
  hours: number;
  publications: number;
  reports: number;
}

export interface AdminReportsOut {
  total_hours: number;
  total_publications: number;
  total_reports: number;
  by_volunteer: VolunteerTotals[];
  reports: ReportOut[];
}

export interface RemindersOut {
  tomorrow: string;
  shifts: ShiftOut[];
}

export interface AnnouncementIn {
  title: string;
  body: string;
  pinned: boolean;
}

export interface Announcement {
  id: string;
  title: string;
  body: string;
  pinned: boolean;
  author_name: string;
  created_at: string;
}
