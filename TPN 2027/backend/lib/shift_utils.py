{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red51\green95\blue50;\red249\green249\blue249;\red45\green45\blue45;
\red103\green38\blue120;\red0\green0\blue0;\red133\green40\blue2;}
{\*\expandedcolortbl;;\cssrgb\c25490\c43922\c25490;\cssrgb\c98039\c98039\c98039;\cssrgb\c23137\c23137\c23137;
\cssrgb\c48627\c23137\c54510;\cssrgb\c0\c0\c0;\cssrgb\c60000\c21961\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 """Shift helpers: time math, serialization, safe removal of a volunteer.\cf4 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 Shape: leader_id (capoturno) + member_ids (max 2, any gender).\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 volunteer_ids = leader + members, kept in sync for overlap / monthly-limit queries.\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 """\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  datetime \cf5 \strokec5 import\cf4 \strokec4  datetime\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  zoneinfo \cf5 \strokec5 import\cf4 \strokec4  ZoneInfo\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  fastapi \cf5 \strokec5 import\cf4 \strokec4  HTTPException\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.db \cf5 \strokec5 import\cf4 \strokec4  db\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  models.schemas \cf5 \strokec5 import\cf4 \strokec4  ShiftOut\strokec6 ,\strokec4  ShiftVolunteer\cb1 \
\
\cb3 MAX_MEMBERS = \cf7 \strokec7 2\cf4 \cb1 \strokec4 \
\cb3 MONTHLY_LIMIT = \cf7 \strokec7 2\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  now_local\strokec6 ()\strokec4  -> \cf5 \strokec5 tuple\cf4 \strokec6 [\cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ]:\cb1 \strokec4 \
\cb3     \cf2 \strokec2 """(YYYY-MM-DD, HH:MM) in APP_TZ."""\cf4 \cb1 \strokec4 \
\cb3     n = datetime.now\strokec6 (\strokec4 ZoneInfo\strokec6 (\strokec4 os.environ.get\strokec6 (\cf2 \strokec2 "APP_TZ"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "UTC"\cf4 \strokec6 )))\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  n.strftime\strokec6 (\cf2 \strokec2 "%Y-%m-%d"\cf4 \strokec6 ),\strokec4  n.strftime\strokec6 (\cf2 \strokec2 "%H:%M"\cf4 \strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  has_ended\strokec6 (\strokec4 s\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 bool\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     d\strokec6 ,\strokec4  t = now_local\strokec6 ()\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  s\strokec6 [\cf2 \strokec2 "date"\cf4 \strokec6 ]\strokec4  < d \cf5 \strokec5 or\cf4 \strokec4  \strokec6 (\strokec4 s\strokec6 [\cf2 \strokec2 "date"\cf4 \strokec6 ]\strokec4  == d \cf5 \strokec5 and\cf4 \strokec4  s\strokec6 [\cf2 \strokec2 "end"\cf4 \strokec6 ]\strokec4  <= t\strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  end_plus_two\strokec6 (\strokec4 start\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 str\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     h\strokec6 ,\strokec4  m = \cf5 \strokec5 map\cf4 \strokec6 (\cf5 \strokec5 int\cf4 \strokec6 ,\strokec4  start.split\strokec6 (\cf2 \strokec2 ":"\cf4 \strokec6 ))\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf2 \strokec2 f"\cf4 \strokec4 \{h + 2\cf2 \strokec2 :02d\cf4 \strokec4 \}\cf2 \strokec2 :\cf4 \strokec4 \{m\cf2 \strokec2 :02d\cf4 \strokec4 \}\cf2 \strokec2 "\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  can_lead\strokec6 (\strokec4 u\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 bool\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Capoturno: a man enabled by an admin. Admins (men) can always lead."""\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  u.get\strokec6 (\cf2 \strokec2 "gender"\cf4 \strokec6 )\strokec4  == \cf2 \strokec2 "M"\cf4 \strokec4  \cf5 \strokec5 and\cf4 \strokec4  \strokec6 (\strokec4 u.get\strokec6 (\cf2 \strokec2 "is_team_leader"\cf4 \strokec6 )\strokec4  \cf5 \strokec5 or\cf4 \strokec4  u.get\strokec6 (\cf2 \strokec2 "role"\cf4 \strokec6 )\strokec4  == \cf2 \strokec2 "admin"\cf4 \strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  serialize\strokec6 (\strokec4 shifts\strokec6 :\strokec4  \cf5 \strokec5 list\cf4 \strokec6 [\cf5 \strokec5 dict\cf4 \strokec6 ],\strokec4  user\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 ,\strokec4  show_phones\strokec6 :\strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 list\cf4 \strokec6 [\strokec4 ShiftOut\strokec6 ]:\cb1 \strokec4 \
\cb3     ids = \cf5 \strokec5 list\cf4 \strokec6 (\{\strokec4 uid \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  shifts \cf5 \strokec5 for\cf4 \strokec4  uid \cf5 \strokec5 in\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 ,\strokec4  \strokec6 [])\})\cb1 \strokec4 \
\cb3     users = \strokec6 \{\cb1 \strokec4 \
\cb3         u\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]:\strokec4  u\cb1 \
\cb3         \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 for\cf4 \strokec4  u \cf5 \strokec5 in\cf4 \strokec4  db.users.find\strokec6 (\{\cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$in"\cf4 \strokec6 :\strokec4  ids\strokec6 \}\},\strokec4  \strokec6 \{\cf2 \strokec2 "_id"\cf4 \strokec6 :\strokec4  \cf7 \strokec7 0\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "password_hash"\cf4 \strokec6 :\strokec4  \cf7 \strokec7 0\cf4 \strokec6 \})\cb1 \strokec4 \
\cb3     \strokec6 \}\cb1 \strokec4 \
\cb3     reported = \strokec6 \{\cb1 \strokec4 \
\cb3         r\strokec6 [\cf2 \strokec2 "shift_id"\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3         \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 for\cf4 \strokec4  r \cf5 \strokec5 in\cf4 \strokec4  db.reports.find\strokec6 (\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "user_id"\cf4 \strokec6 :\strokec4  user\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ],\strokec4  \cf2 \strokec2 "shift_id"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$in"\cf4 \strokec6 :\strokec4  \strokec6 [\strokec4 s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\strokec4  \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  shifts\strokec6 ]\}\},\strokec4  \strokec6 \{\cf2 \strokec2 "shift_id"\cf4 \strokec6 :\strokec4  \cf7 \strokec7 1\cf4 \strokec6 \}\cb1 \strokec4 \
\cb3         \strokec6 )\cb1 \strokec4 \
\cb3     \strokec6 \}\cb1 \strokec4 \
\cb3     phones = user\strokec6 [\cf2 \strokec2 "role"\cf4 \strokec6 ]\strokec4  == \cf2 \strokec2 "admin"\cf4 \strokec4  \cf5 \strokec5 or\cf4 \strokec4  show_phones\cb1 \
\
\cb3     \cf5 \strokec5 def\cf4 \strokec4  vol\strokec6 (\strokec4 uid\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec4  | \cf5 \strokec5 None\cf4 \strokec6 )\strokec4  -> ShiftVolunteer | \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         u = users.get\strokec6 (\strokec4 uid\strokec6 )\strokec4  \cf5 \strokec5 if\cf4 \strokec4  uid \cf5 \strokec5 else\cf4 \strokec4  \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  u\strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  ShiftVolunteer\strokec6 (\cb1 \strokec4 \
\cb3             \cf5 \strokec5 id\cf4 \strokec4 =uid\strokec6 ,\strokec4  first_name=u.get\strokec6 (\cf2 \strokec2 "first_name"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 ""\cf4 \strokec6 ),\strokec4  last_name=u.get\strokec6 (\cf2 \strokec2 "last_name"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 ""\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3             gender=u.get\strokec6 (\cf2 \strokec2 "gender"\cf4 \strokec6 ),\strokec4  phone=u.get\strokec6 (\cf2 \strokec2 "phone"\cf4 \strokec6 )\strokec4  \cf5 \strokec5 if\cf4 \strokec4  phones \cf5 \strokec5 else\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3         \strokec6 )\cb1 \strokec4 \
\
\cb3     out\strokec6 :\strokec4  \cf5 \strokec5 list\cf4 \strokec6 [\strokec4 ShiftOut\strokec6 ]\strokec4  = \strokec6 []\cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  shifts\strokec6 :\cb1 \strokec4 \
\cb3         leader = vol\strokec6 (\strokec4 s.get\strokec6 (\cf2 \strokec2 "leader_id"\cf4 \strokec6 ))\cb1 \strokec4 \
\cb3         members = \strokec6 [\strokec4 v \cf5 \strokec5 for\cf4 \strokec4  uid \cf5 \strokec5 in\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "member_ids"\cf4 \strokec6 ,\strokec4  \strokec6 [])\strokec4  \cf5 \strokec5 if\cf4 \strokec4  \strokec6 (\strokec4 v \strokec6 :\strokec4 = vol\strokec6 (\strokec4 uid\strokec6 ))]\cb1 \strokec4 \
\cb3         free_members = \cf5 \strokec5 max\cf4 \strokec6 (\cf7 \strokec7 0\cf4 \strokec6 ,\strokec4  MAX_MEMBERS - \cf5 \strokec5 len\cf4 \strokec6 (\strokec4 s.get\strokec6 (\cf2 \strokec2 "member_ids"\cf4 \strokec6 ,\strokec4  \strokec6 [])))\cb1 \strokec4 \
\cb3         missing_leader = \cf5 \strokec5 not\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "leader_id"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         my_role = \cf2 \strokec2 "leader"\cf4 \strokec4  \cf5 \strokec5 if\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "leader_id"\cf4 \strokec6 )\strokec4  == user\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\strokec4  \cf5 \strokec5 else\cf4 \strokec4  \strokec6 (\cf2 \strokec2 "member"\cf4 \strokec4  \cf5 \strokec5 if\cf4 \strokec4  user\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\strokec4  \cf5 \strokec5 in\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "member_ids"\cf4 \strokec6 ,\strokec4  \strokec6 [])\strokec4  \cf5 \strokec5 else\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         out.append\strokec6 (\strokec4 ShiftOut\strokec6 (\cb1 \strokec4 \
\cb3             \cf5 \strokec5 id\cf4 \strokec4 =s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ],\strokec4  station=s\strokec6 [\cf2 \strokec2 "station"\cf4 \strokec6 ],\strokec4  date=s\strokec6 [\cf2 \strokec2 "date"\cf4 \strokec6 ],\strokec4  start=s\strokec6 [\cf2 \strokec2 "start"\cf4 \strokec6 ],\strokec4  end=s\strokec6 [\cf2 \strokec2 "end"\cf4 \strokec6 ],\cb1 \strokec4 \
\cb3             leader=leader\strokec6 ,\strokec4  members=members\strokec6 ,\strokec4  missing_leader=missing_leader\strokec6 ,\cb1 \strokec4 \
\cb3             free_member_slots=free_members\strokec6 ,\strokec4  free_slots=free_members + \strokec6 (\cf7 \strokec7 1\cf4 \strokec4  \cf5 \strokec5 if\cf4 \strokec4  missing_leader \cf5 \strokec5 else\cf4 \strokec4  \cf7 \strokec7 0\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3             is_complete=\cf5 \strokec5 not\cf4 \strokec4  missing_leader \cf5 \strokec5 and\cf4 \strokec4  free_members == \cf7 \strokec7 0\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3             is_mine=my_role \cf5 \strokec5 is\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 ,\strokec4  my_role=my_role\strokec6 ,\cb1 \strokec4 \
\cb3             has_ended=has_ended\strokec6 (\strokec4 s\strokec6 ),\strokec4  my_report_done=s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\strokec4  \cf5 \strokec5 in\cf4 \strokec4  reported\strokec6 ,\cb1 \strokec4 \
\cb3         \strokec6 ))\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  out\cb1 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  remove_volunteer\strokec6 (\strokec4 shift_filter\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 ,\strokec4  uid\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 int\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Remove uid from matching shifts (as leader or member). Returns modified count."""\cf4 \cb1 \strokec4 \
\cb3     res = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.update_many\strokec6 (\cb1 \strokec4 \
\cb3         \strokec6 \{\strokec4 **shift_filter\strokec6 ,\strokec4  \cf2 \strokec2 "member_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "$pull"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "member_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 ,\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\}\cb1 \strokec4 \
\cb3     \strokec6 )\cb1 \strokec4 \
\cb3     res2 = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.update_many\strokec6 (\cb1 \strokec4 \
\cb3         \strokec6 \{\strokec4 **shift_filter\strokec6 ,\strokec4  \cf2 \strokec2 "leader_id"\cf4 \strokec6 :\strokec4  uid\strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "$set"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "leader_id"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 None\cf4 \strokec6 \},\strokec4  \cf2 \strokec2 "$pull"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\}\cb1 \strokec4 \
\cb3     \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  res.modified_count + res2.modified_count\cb1 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  month_usage\strokec6 (\strokec4 uid\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  date\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 int\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 await\cf4 \strokec4  db.shifts.count_documents\strokec6 (\{\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 ,\strokec4  \cf2 \strokec2 "date"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$regex"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 f"^\cf4 \strokec4 \{date[\cf2 \strokec2 :7]\cf4 \strokec4 \}\cf2 \strokec2 -"\cf4 \strokec6 \}\})\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  place\strokec6 (\strokec4 s\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 ,\strokec4  target\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 ,\strokec4  as_role\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  *\strokec6 ,\strokec4  enforce_monthly\strokec6 :\strokec4  \cf5 \strokec5 bool\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Atomically put `target` into shift `s` in `as_role`, enforcing seat, capoturno, overlap (and monthly) rules."""\cf4 \cb1 \strokec4 \
\cb3     uid = target\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  uid \cf5 \strokec5 in\cf4 \strokec4  s.get\strokec6 (\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 ,\strokec4  \strokec6 []):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 409\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Gi\'e0 iscritto a questo turno"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  enforce_monthly \cf5 \strokec5 and\cf4 \strokec4  \cf5 \strokec5 await\cf4 \strokec4  month_usage\strokec6 (\strokec4 uid\strokec6 ,\strokec4  s\strokec6 [\cf2 \strokec2 "date"\cf4 \strokec6 ])\strokec4  >= MONTHLY_LIMIT\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 409\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 f"Hai gi\'e0 raggiunto il limite di \cf4 \strokec4 \{MONTHLY_LIMIT\}\cf2 \strokec2  turni per questo mese"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     overlap = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.find_one\strokec6 (\{\cb1 \strokec4 \
\cb3         \cf2 \strokec2 "date"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "date"\cf4 \strokec6 ],\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 ,\strokec4  \cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$ne"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ]\},\cb1 \strokec4 \
\cb3         \cf2 \strokec2 "start"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$lt"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "end"\cf4 \strokec6 ]\},\strokec4  \cf2 \strokec2 "end"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$gt"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "start"\cf4 \strokec6 ]\},\cb1 \strokec4 \
\cb3     \strokec6 \})\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  overlap\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 409\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 f"Gi\'e0 iscritto a un turno sovrapposto (\cf4 \strokec4 \{overlap['start']\}\cf2 \strokec2 -\cf4 \strokec4 \{overlap['end']\}\cf2 \strokec2 )"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  as_role == \cf2 \strokec2 "leader"\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  can_lead\strokec6 (\strokec4 target\strokec6 ):\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 403\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Solo gli uomini abilitati come capoturno possono ricoprire questo ruolo"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         res = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.update_one\strokec6 (\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ],\strokec4  \cf2 \strokec2 "leader_id"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 None\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$ne"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\},\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "$set"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "leader_id"\cf4 \strokec6 :\strokec4  uid\strokec6 \},\strokec4  \cf2 \strokec2 "$push"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\},\cb1 \strokec4 \
\cb3         \strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  res.modified_count\strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 409\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Il posto di capoturno \'e8 gi\'e0 occupato"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 else\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         res = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.update_one\strokec6 (\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "id"\cf4 \strokec6 ],\strokec4  \cf2 \strokec2 f"member_ids.\cf4 \strokec4 \{MAX_MEMBERS - 1\}\cf2 \strokec2 "\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$exists"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 False\cf4 \strokec6 \},\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$ne"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\},\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "$push"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "member_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 ,\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  uid\strokec6 \}\},\cb1 \strokec4 \
\cb3         \strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  res.modified_count\strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 409\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Posti volontario esauriti: resta libero solo il posto di capoturno"\cf4 \strokec6 )\cb1 \strokec4 \
\
}