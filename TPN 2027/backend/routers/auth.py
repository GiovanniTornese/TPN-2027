{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red157\green88\blue173;\red16\green16\blue16;\red187\green187\blue187;
\red212\green212\blue212;\red80\green173\blue77;\red191\green91\blue43;\red70\green137\blue204;}
{\*\expandedcolortbl;;\cssrgb\c68235\c44314\c73333;\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;
\cssrgb\c86275\c86275\c86275;\cssrgb\c37255\c72157\c37255;\cssrgb\c80000\c43922\c21961;\cssrgb\c33725\c61176\c83922;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf4 \strokec4  uuid\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  datetime \cf2 \strokec2 import\cf4 \strokec4  datetime\cf5 \strokec5 ,\cf4 \strokec4  timezone\cb1 \
\
\cf2 \cb3 \strokec2 import\cf4 \strokec4  httpx\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  fastapi \cf2 \strokec2 import\cf4 \strokec4  APIRouter\cf5 \strokec5 ,\cf4 \strokec4  Depends\cf5 \strokec5 ,\cf4 \strokec4  HTTPException\cf5 \strokec5 ,\cf4 \strokec4  Response\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.auth \cf2 \strokec2 import\cf4 \strokec4  clear_session\cf5 \strokec5 ,\cf4 \strokec4  current_user\cf5 \strokec5 ,\cf4 \strokec4  hash_pw\cf5 \strokec5 ,\cf4 \strokec4  set_session\cf5 \strokec5 ,\cf4 \strokec4  verify_pw\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.dates \cf2 \strokec2 import\cf4 \strokec4  today_iso\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.db \cf2 \strokec2 import\cf4 \strokec4  db\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  models.schemas \cf2 \strokec2 import\cf4 \strokec4  CredentialsIn\cf5 \strokec5 ,\cf4 \strokec4  GoogleSessionIn\cf5 \strokec5 ,\cf4 \strokec4  LoginIn\cf5 \strokec5 ,\cf4 \strokec4  ProfileIn\cf5 \strokec5 ,\cf4 \strokec4  RegisterIn\cf5 \strokec5 ,\cf4 \strokec4  UserPublic\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 router = APIRouter\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3 EMERGENT_SESSION_URL = \cf6 \strokec6 "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf4 \strokec4  public\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf5 \strokec5 )\cf4 \strokec4  -> UserPublic\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 return\cf4 \strokec4  UserPublic.model_validate\cf5 \strokec5 (\{\cf4 \strokec4 **user\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "has_password"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 bool\cf5 \strokec5 (\cf4 \strokec4 user.get\cf5 \strokec5 (\cf6 \strokec6 "password_hash"\cf5 \strokec5 ))\})\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  has_upcoming_shifts\cf5 \strokec5 (\cf4 \strokec4 uid\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 bool\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf2 \strokec2 bool\cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  db.shifts.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "volunteer_ids"\cf5 \strokec5 :\cf4 \strokec4  uid\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\}\}))\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  check_gender_change\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf5 \strokec5 ,\cf4 \strokec4  new_gender\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 None\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 if\cf4 \strokec4  user.get\cf5 \strokec5 (\cf6 \strokec6 "gender"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 and\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "gender"\cf5 \strokec5 ]\cf4 \strokec4  != new_gender \cf2 \strokec2 and\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  has_upcoming_shifts\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ]):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Impossibile cambiare genere con iscrizioni a turni futuri: annullale prima."\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf4 \strokec4  new_volunteer_doc\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  RegisterIn\cf5 \strokec5 ,\cf4 \strokec4  is_team_leader\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 bool\cf4 \strokec4  = \cf2 \strokec2 False\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 dict\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 (\cf4 \strokec4 uuid.uuid4\cf5 \strokec5 ()),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  body.email.lower\cf5 \strokec5 (),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "password_hash"\cf5 \strokec5 :\cf4 \strokec4  hash_pw\cf5 \strokec5 (\cf4 \strokec4 body.password\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "role"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "volunteer"\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "first_name"\cf5 \strokec5 :\cf4 \strokec4  body.first_name.strip\cf5 \strokec5 (),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "last_name"\cf5 \strokec5 :\cf4 \strokec4  body.last_name.strip\cf5 \strokec5 (),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "phone"\cf5 \strokec5 :\cf4 \strokec4  body.phone.strip\cf5 \strokec5 (),\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "gender"\cf5 \strokec5 :\cf4 \strokec4  body.gender\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "is_team_leader"\cf5 \strokec5 :\cf4 \strokec4  is_team_leader \cf2 \strokec2 and\cf4 \strokec4  body.gender == \cf6 \strokec6 "M"\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "created_at"\cf5 \strokec5 :\cf4 \strokec4  datetime.now\cf5 \strokec5 (\cf4 \strokec4 timezone.utc\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/auth/register"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  register\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  RegisterIn\cf5 \strokec5 ,\cf4 \strokec4  response\cf5 \strokec5 :\cf4 \strokec4  Response\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  body.email.lower\cf5 \strokec5 ()\}):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Email gi\'e0 registrata"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     doc = new_volunteer_doc\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.insert_one\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     set_session\cf5 \strokec5 (\cf4 \strokec4 response\cf5 \strokec5 ,\cf4 \strokec4  doc\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/auth/login"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  login\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  LoginIn\cf5 \strokec5 ,\cf4 \strokec4  response\cf5 \strokec5 :\cf4 \strokec4  Response\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     user = \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  body.email.lower\cf5 \strokec5 ()\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  user \cf2 \strokec2 or\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  verify_pw\cf5 \strokec5 (\cf4 \strokec4 body.password\cf5 \strokec5 ,\cf4 \strokec4  user.get\cf5 \strokec5 (\cf6 \strokec6 "password_hash"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 401\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Email o password non corretti"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     set_session\cf5 \strokec5 (\cf4 \strokec4 response\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/auth/google"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  google_login\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  GoogleSessionIn\cf5 \strokec5 ,\cf4 \strokec4  response\cf5 \strokec5 :\cf4 \strokec4  Response\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf6 \strokec6 """Exchange Emergent Google-auth session_id for our own cookie session (find-or-create by email)."""\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 with\cf4 \strokec4  httpx.AsyncClient\cf5 \strokec5 (\cf4 \strokec4 timeout=\cf7 \strokec7 15\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  client\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         r = \cf2 \strokec2 await\cf4 \strokec4  client.get\cf5 \strokec5 (\cf4 \strokec4 EMERGENT_SESSION_URL\cf5 \strokec5 ,\cf4 \strokec4  headers=\cf5 \strokec5 \{\cf6 \strokec6 "X-Session-ID"\cf5 \strokec5 :\cf4 \strokec4  body.session_id\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  r.status_code != \cf7 \strokec7 200\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 401\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Accesso con Google non riuscito"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     data = r.json\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     email = \cf5 \strokec5 (\cf4 \strokec4 data.get\cf5 \strokec5 (\cf6 \strokec6 "email"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 or\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 )\cf4 \strokec4 .lower\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  email\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 401\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Accesso con Google non riuscito"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     user = \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  email\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         parts = \cf5 \strokec5 (\cf4 \strokec4 data.get\cf5 \strokec5 (\cf6 \strokec6 "name"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 or\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 )\cf4 \strokec4 .strip\cf5 \strokec5 ()\cf4 \strokec4 .split\cf5 \strokec5 (\cf6 \strokec6 " "\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3         user = \cf5 \strokec5 \{\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 (\cf4 \strokec4 uuid.uuid4\cf5 \strokec5 ()),\cf4 \strokec4  \cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  email\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "password_hash"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "role"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "volunteer"\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "first_name"\cf5 \strokec5 :\cf4 \strokec4  parts\cf5 \strokec5 [\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  parts \cf2 \strokec2 else\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "last_name"\cf5 \strokec5 :\cf4 \strokec4  parts\cf5 \strokec5 [\cf7 \strokec7 1\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 len\cf5 \strokec5 (\cf4 \strokec4 parts\cf5 \strokec5 )\cf4 \strokec4  > \cf7 \strokec7 1\cf4 \strokec4  \cf2 \strokec2 else\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "phone"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 ""\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "gender"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 None\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "is_team_leader"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 False\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "created_at"\cf5 \strokec5 :\cf4 \strokec4  datetime.now\cf5 \strokec5 (\cf4 \strokec4 timezone.utc\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 await\cf4 \strokec4  db.users.insert_one\cf5 \strokec5 (\cf2 \strokec2 dict\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 ))\cf4 \cb1 \strokec4 \
\cb3     set_session\cf5 \strokec5 (\cf4 \strokec4 response\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/auth/logout"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  logout\cf5 \strokec5 (\cf4 \strokec4 response\cf5 \strokec5 :\cf4 \strokec4  Response\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     clear_session\cf5 \strokec5 (\cf4 \strokec4 response\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "ok"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/auth/me"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  me\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/me"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  update_profile\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  ProfileIn\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 await\cf4 \strokec4  check_gender_change\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 ,\cf4 \strokec4  body.gender\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     data\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = \cf5 \strokec5 \{\cf4 \strokec4 k\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 (\cf4 \strokec4 v.strip\cf5 \strokec5 ()\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 isinstance\cf5 \strokec5 (\cf4 \strokec4 v\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 else\cf4 \strokec4  v\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  k\cf5 \strokec5 ,\cf4 \strokec4  v \cf2 \strokec2 in\cf4 \strokec4  body.model_dump\cf5 \strokec5 ()\cf4 \strokec4 .items\cf5 \strokec5 ()\}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.gender == \cf6 \strokec6 "F"\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         data\cf5 \strokec5 [\cf6 \strokec6 "is_team_leader"\cf5 \strokec5 ]\cf4 \strokec4  = \cf2 \strokec2 False\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ]\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\{\cf4 \strokec4 **user\cf5 \strokec5 ,\cf4 \strokec4  **data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/me/credentials"\cf5 \strokec5 ,\cf4 \strokec4  response_model=UserPublic\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  update_credentials\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  CredentialsIn\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 if\cf4 \strokec4  user.get\cf5 \strokec5 (\cf6 \strokec6 "password_hash"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 and\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  verify_pw\cf5 \strokec5 (\cf4 \strokec4 body.current_password\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "password_hash"\cf5 \strokec5 ]):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Password attuale non corretta"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     email = body.email.lower\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     data\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = \cf5 \strokec5 \{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  email\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  email != user\cf5 \strokec5 [\cf6 \strokec6 "email"\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 and\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "email"\cf5 \strokec5 :\cf4 \strokec4  email\cf5 \strokec5 \}):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Email gi\'e0 in uso da un altro account"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.new_password\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         data\cf5 \strokec5 [\cf6 \strokec6 "password_hash"\cf5 \strokec5 ]\cf4 \strokec4  = hash_pw\cf5 \strokec5 (\cf4 \strokec4 body.new_password\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.users.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ]\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  public\cf5 \strokec5 (\{\cf4 \strokec4 **user\cf5 \strokec5 ,\cf4 \strokec4  **data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\
}