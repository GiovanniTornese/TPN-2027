{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red157\green88\blue173;\red16\green16\blue16;\red187\green187\blue187;
\red212\green212\blue212;\red80\green173\blue77;\red191\green91\blue43;\red70\green137\blue204;\red71\green71\blue71;
}
{\*\expandedcolortbl;;\cssrgb\c68235\c44314\c73333;\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;
\cssrgb\c86275\c86275\c86275;\cssrgb\c37255\c72157\c37255;\cssrgb\c80000\c43922\c21961;\cssrgb\c33725\c61176\c83922;\cssrgb\c34902\c34902\c34902;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 from\cf4 \strokec4  fastapi \cf2 \strokec2 import\cf4 \strokec4  APIRouter\cf5 \strokec5 ,\cf4 \strokec4  Depends\cf5 \strokec5 ,\cf4 \strokec4  HTTPException\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.auth \cf2 \strokec2 import\cf4 \strokec4  hash_pw\cf5 \strokec5 ,\cf4 \strokec4  require_admin\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.dates \cf2 \strokec2 import\cf4 \strokec4  today_iso\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.db \cf2 \strokec2 import\cf4 \strokec4  db\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.shift_utils \cf2 \strokec2 import\cf4 \strokec4  remove_volunteer\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  models.schemas \cf2 \strokec2 import\cf4 \strokec4  VolunteerAdminIn\cf5 \strokec5 ,\cf4 \strokec4  VolunteerCreateIn\cf5 \strokec5 ,\cf4 \strokec4  VolunteerOut\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  routers.auth \cf2 \strokec2 import\cf4 \strokec4  check_gender_change\cf5 \strokec5 ,\cf4 \strokec4  new_volunteer_doc\cb1 \
\
\cb3 router = APIRouter\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\
\
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  counts\cf5 \strokec5 (\cf4 \strokec4 field_filter\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 dict\cf5 \strokec5 [\cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 int\cf5 \strokec5 ]:\cf4 \cb1 \strokec4 \
\cb3     pipeline = \cf5 \strokec5 [\{\cf6 \strokec6 "$match"\cf5 \strokec5 :\cf4 \strokec4  field_filter\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$unwind"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "$volunteer_ids"\cf5 \strokec5 \},\cf4 \cb1 \strokec4 \
\cb3                 \cf5 \strokec5 \{\cf6 \strokec6 "$group"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "$volunteer_ids"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "n"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$sum"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 \}\}\}]\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf4 \strokec4 d\cf5 \strokec5 [\cf6 \strokec6 "_id"\cf5 \strokec5 ]:\cf4 \strokec4  d\cf5 \strokec5 [\cf6 \strokec6 "n"\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  d \cf2 \strokec2 in\cf4 \strokec4  db.shifts.aggregate\cf5 \strokec5 (\cf4 \strokec4 pipeline\cf5 \strokec5 )\}\cf4 \cb1 \strokec4 \
\
\
\cf2 \cb3 \strokec2 def\cf4 \strokec4  out\cf5 \strokec5 (\cf4 \strokec4 u\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf5 \strokec5 ,\cf4 \strokec4  **extra\cf5 \strokec5 )\cf4 \strokec4  -> VolunteerOut\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  VolunteerOut.model_validate\cf5 \strokec5 (\{\cf4 \strokec4 **u\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "has_password"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 bool\cf5 \strokec5 (\cf4 \strokec4 u.get\cf5 \strokec5 (\cf6 \strokec6 "password_hash"\cf5 \strokec5 )),\cf4 \strokec4  **extra\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/volunteers"\cf5 \strokec5 ,\cf4 \strokec4  response_model=\cf2 \strokec2 list\cf5 \strokec5 [\cf4 \strokec4 VolunteerOut\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  list_volunteers\cf5 \strokec5 (\cf4 \strokec4 include_admins\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 bool\cf4 \strokec4  = \cf2 \strokec2 False\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     roles = \cf5 \strokec5 [\cf6 \strokec6 "volunteer"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "admin"\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  include_admins \cf2 \strokec2 else\cf4 \strokec4  \cf5 \strokec5 [\cf6 \strokec6 "volunteer"\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\cb3     users = \cf2 \strokec2 await\cf4 \strokec4  db.users.find\cf5 \strokec5 (\{\cf6 \strokec6 "role"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$in"\cf5 \strokec5 :\cf4 \strokec4  roles\cf5 \strokec5 \}\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \strokec4  \\\cb1 \
\cb3         .sort\cf5 \strokec5 ([(\cf6 \strokec6 "last_name"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "first_name"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )])\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf7 \strokec7 5000\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     total = \cf2 \strokec2 await\cf4 \strokec4  counts\cf5 \strokec5 (\{\})\cf4 \cb1 \strokec4 \
\cb3     upcoming = \cf2 \strokec2 await\cf4 \strokec4  counts\cf5 \strokec5 (\{\cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\}\})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 [\cf4 \strokec4 out\cf5 \strokec5 (\cf4 \strokec4 u\cf5 \strokec5 ,\cf4 \strokec4  shift_count=total.get\cf5 \strokec5 (\cf4 \strokec4 u\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ],\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 ),\cf4 \strokec4  upcoming_count=upcoming.get\cf5 \strokec5 (\cf4 \strokec4 u\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ],\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 ))\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  u \cf2 \strokec2 in\cf4 \strokec4  users\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/volunteers"\cf5 \strokec5 ,\cf4 \strokec4  response_model=VolunteerOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  create_volunteer\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  VolunteerCreateIn\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  body.email.lower\cf5 \strokec5 ()\}):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Email gi\'e0 registrata"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     doc = new_volunteer_doc\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 ,\cf4 \strokec4  body.is_team_leader\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.insert_one\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  out\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  load_volunteer\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 dict\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3     u = \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  uid\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "role"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "volunteer"\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  u\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Volontario non trovato"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  u\cb1 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/volunteers/\{uid\}"\cf5 \strokec5 ,\cf4 \strokec4  response_model=VolunteerOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  update_volunteer\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  body\cf5 \strokec5 :\cf4 \strokec4  VolunteerAdminIn\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     u = \cf2 \strokec2 await\cf4 \strokec4  load_volunteer\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  check_gender_change\cf5 \strokec5 (\cf4 \strokec4 u\cf5 \strokec5 ,\cf4 \strokec4  body.gender\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.is_team_leader \cf2 \strokec2 and\cf4 \strokec4  body.gender != \cf6 \strokec6 "M"\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Il capoturno deve essere un uomo"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  body.is_team_leader \cf2 \strokec2 and\cf4 \strokec4  u.get\cf5 \strokec5 (\cf6 \strokec6 "is_team_leader"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 and\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find_one\cf5 \strokec5 (\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 \{\cf6 \strokec6 "leader_id"\cf5 \strokec5 :\cf4 \strokec4  uid\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\}\}\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "\'c8 capoturno in turni futuri: rimuovilo prima da quei turni"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     data = \cf5 \strokec5 \{\cf4 \strokec4 k\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 (\cf4 \strokec4 v.strip\cf5 \strokec5 ()\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 isinstance\cf5 \strokec5 (\cf4 \strokec4 v\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 else\cf4 \strokec4  v\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  k\cf5 \strokec5 ,\cf4 \strokec4  v \cf2 \strokec2 in\cf4 \strokec4  body.model_dump\cf5 \strokec5 (\cf4 \strokec4 exclude=\cf5 \strokec5 \{\cf6 \strokec6 "email"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "new_password"\cf5 \strokec5 \})\cf4 \strokec4 .items\cf5 \strokec5 ()\}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.email \cf2 \strokec2 and\cf4 \strokec4  body.email.lower\cf5 \strokec5 ()\cf4 \strokec4  != u\cf5 \strokec5 [\cf6 \strokec6 "email"\cf5 \strokec5 ]:\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  body.email.lower\cf5 \strokec5 ()\}):\cf4 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Email gi\'e0 in uso da un altro account"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3         data\cf5 \strokec5 [\cf6 \strokec6 "email"\cf5 \strokec5 ]\cf4 \strokec4  = body.email.lower\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.new_password\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         data\cf5 \strokec5 [\cf6 \strokec6 "password_hash"\cf5 \strokec5 ]\cf4 \strokec4  = hash_pw\cf5 \strokec5 (\cf4 \strokec4 body.new_password\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  uid\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  out\cf5 \strokec5 (\{\cf4 \strokec4 **u\cf5 \strokec5 ,\cf4 \strokec4  **data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .delete\cf5 \strokec5 (\cf6 \strokec6 "/volunteers/\{uid\}"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  delete_volunteer\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  load_volunteer\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  remove_volunteer\cf5 \strokec5 (\{\},\cf4 \strokec4  uid\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.delete_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  uid\cf5 \strokec5 \})\cf4 \strokec4   \cf9 \strokec9 # reports are kept so association totals don't change\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "ok"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\
}