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
\cf2 \cb3 \strokec2 from\cf4 \strokec4  datetime \cf2 \strokec2 import\cf4 \strokec4  date \cf2 \strokec2 as\cf4 \strokec4  Date\cf5 \strokec5 ,\cf4 \strokec4  timedelta\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  typing \cf2 \strokec2 import\cf4 \strokec4  Optional\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  fastapi \cf2 \strokec2 import\cf4 \strokec4  APIRouter\cf5 \strokec5 ,\cf4 \strokec4  Depends\cf5 \strokec5 ,\cf4 \strokec4  HTTPException\cf5 \strokec5 ,\cf4 \strokec4  Query\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  pymongo.errors \cf2 \strokec2 import\cf4 \strokec4  DuplicateKeyError\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.auth \cf2 \strokec2 import\cf4 \strokec4  current_user\cf5 \strokec5 ,\cf4 \strokec4  require_admin\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.dates \cf2 \strokec2 import\cf4 \strokec4  today_iso\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.db \cf2 \strokec2 import\cf4 \strokec4  db\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.shift_utils \cf2 \strokec2 import\cf4 \strokec4  MAX_MEMBERS\cf5 \strokec5 ,\cf4 \strokec4  MONTHLY_LIMIT\cf5 \strokec5 ,\cf4 \strokec4  month_usage\cf5 \strokec5 ,\cf4 \strokec4  place\cf5 \strokec5 ,\cf4 \strokec4  remove_volunteer\cf5 \strokec5 ,\cf4 \strokec4  serialize\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  models.schemas \cf2 \strokec2 import\cf4 \strokec4  \cf5 \strokec5 (\cf4 \cb1 \strokec4 \
\cb3     DATE_PATTERN\cf5 \strokec5 ,\cf4 \strokec4  AssignIn\cf5 \strokec5 ,\cf4 \strokec4  JoinIn\cf5 \strokec5 ,\cf4 \strokec4  MonthUsageOut\cf5 \strokec5 ,\cf4 \strokec4  RemindersOut\cf5 \strokec5 ,\cf4 \strokec4  ShiftBulkOut\cf5 \strokec5 ,\cf4 \strokec4  ShiftCreateIn\cf5 \strokec5 ,\cf4 \strokec4  ShiftIn\cf5 \strokec5 ,\cf4 \strokec4  ShiftOut\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 )\cf4 \cb1 \strokec4 \
\
\cb3 router = APIRouter\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3 DUP_MSG = \cf6 \strokec6 "Esiste gi\'e0 un turno per questa postazione, data e orario"\cf4 \cb1 \strokec4 \
\cb3 MAX_REPEATS = \cf7 \strokec7 60\cf4 \cb1 \strokec4 \
\
\
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 dict\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3     s = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  s\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Turno non trovato"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  s\cb1 \
\
\
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  check_station\cf5 \strokec5 (\cf4 \strokec4 key\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 )\cf4 \strokec4  -> \cf2 \strokec2 None\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.stations.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  key\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$ne"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\}):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Postazione non valida"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/shifts"\cf5 \strokec5 ,\cf4 \strokec4  response_model=\cf2 \strokec2 list\cf5 \strokec5 [\cf4 \strokec4 ShiftOut\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  list_shifts\cf5 \strokec5 (\cf4 \cb1 \strokec4 \
\cb3     start\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf4 \strokec4  = Query\cf5 \strokec5 (\cf4 \strokec4 pattern=DATE_PATTERN\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cb3     end\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf4 \strokec4  = Query\cf5 \strokec5 (\cf4 \strokec4 pattern=DATE_PATTERN\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cb3     station\cf5 \strokec5 :\cf4 \strokec4  Optional\cf5 \strokec5 [\cf2 \strokec2 str\cf5 \strokec5 ]\cf4 \strokec4  = \cf2 \strokec2 None\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3     user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 ),\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 ):\cf4 \cb1 \strokec4 \
\cb3     q\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = \cf5 \strokec5 \{\cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  start\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "$lte"\cf5 \strokec5 :\cf4 \strokec4  end\cf5 \strokec5 \}\}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  station\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         q\cf5 \strokec5 [\cf6 \strokec6 "station"\cf5 \strokec5 ]\cf4 \strokec4  = station\cb1 \
\cb3     docs = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find\cf5 \strokec5 (\cf4 \strokec4 q\cf5 \strokec5 ,\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \strokec4 .sort\cf5 \strokec5 ([(\cf6 \strokec6 "date"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "start"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "station"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )])\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf7 \strokec7 2000\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 (\cf4 \strokec4 docs\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/shifts/my-usage"\cf5 \strokec5 ,\cf4 \strokec4  response_model=MonthUsageOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  my_usage\cf5 \strokec5 (\cf4 \strokec4 month\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf4 \strokec4  = Query\cf5 \strokec5 (\cf4 \strokec4 pattern=r\cf6 \strokec6 "^\\d\{4\}-\\d\{2\}$"\cf5 \strokec5 ),\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  MonthUsageOut\cf5 \strokec5 (\cf4 \strokec4 month=month\cf5 \strokec5 ,\cf4 \strokec4  used=\cf2 \strokec2 await\cf4 \strokec4  month_usage\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ],\cf4 \strokec4  \cf6 \strokec6 f"\cf4 \strokec4 \{month\}\cf6 \strokec6 -01"\cf5 \strokec5 ),\cf4 \strokec4  limit=MONTHLY_LIMIT\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/shifts/leading"\cf5 \strokec5 ,\cf4 \strokec4  response_model=\cf2 \strokec2 list\cf5 \strokec5 [\cf4 \strokec4 ShiftOut\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  my_leading_shifts\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 """Upcoming shifts where the caller is capoturno \'97 includes the members' phone numbers."""\cf4 \cb1 \strokec4 \
\cb3     docs = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find\cf5 \strokec5 (\{\cf6 \strokec6 "leader_id"\cf5 \strokec5 :\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ],\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\}\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \strokec4  \\\cb1 \
\cb3         .sort\cf5 \strokec5 ([(\cf6 \strokec6 "date"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "start"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )])\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf7 \strokec7 200\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 (\cf4 \strokec4 docs\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 ,\cf4 \strokec4  show_phones=\cf2 \strokec2 True\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/shifts/uncovered"\cf5 \strokec5 ,\cf4 \strokec4  response_model=\cf2 \strokec2 list\cf5 \strokec5 [\cf4 \strokec4 ShiftOut\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  uncovered_shifts\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 """Upcoming shifts still missing the capoturno or one of the two volunteers."""\cf4 \cb1 \strokec4 \
\cb3     q = \cf5 \strokec5 \{\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\},\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "$or"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 [\{\cf6 \strokec6 "leader_id"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 None\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 f"member_ids.\cf4 \strokec4 \{MAX_MEMBERS - 1\}\cf6 \strokec6 "\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$exists"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 False\cf5 \strokec5 \}\}],\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3     docs = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find\cf5 \strokec5 (\cf4 \strokec4 q\cf5 \strokec5 ,\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \strokec4 .sort\cf5 \strokec5 ([(\cf6 \strokec6 "date"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "start"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 ),\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "station"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )])\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf7 \strokec7 1000\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 (\cf4 \strokec4 docs\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/me/reminders"\cf5 \strokec5 ,\cf4 \strokec4  response_model=RemindersOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  my_reminders\cf5 \strokec5 (\cf4 \strokec4 user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 """In-app reminder: the caller's shifts happening tomorrow."""\cf4 \cb1 \strokec4 \
\cb3     tomorrow = \cf5 \strokec5 (\cf4 \strokec4 Date.fromisoformat\cf5 \strokec5 (\cf4 \strokec4 today_iso\cf5 \strokec5 ())\cf4 \strokec4  + timedelta\cf5 \strokec5 (\cf4 \strokec4 days=\cf7 \strokec7 1\cf5 \strokec5 ))\cf4 \strokec4 .isoformat\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     docs = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.find\cf5 \strokec5 (\{\cf6 \strokec6 "volunteer_ids"\cf5 \strokec5 :\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ],\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  tomorrow\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \strokec4 .sort\cf5 \strokec5 (\cf6 \strokec6 "start"\cf5 \strokec5 ,\cf4 \strokec4  \cf7 \strokec7 1\cf5 \strokec5 )\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf7 \strokec7 20\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  RemindersOut\cf5 \strokec5 (\cf4 \strokec4 tomorrow=tomorrow\cf5 \strokec5 ,\cf4 \strokec4  shifts=\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 (\cf4 \strokec4 docs\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 ))\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/shifts"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftBulkOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  create_shift\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  ShiftCreateIn\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  check_station\cf5 \strokec5 (\cf4 \strokec4 body.station\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     dates = \cf5 \strokec5 [\cf4 \strokec4 body.date\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.repeat_until\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  body.repeat_until < body.date\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "La data di fine ripetizione deve essere successiva alla data del turno"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3         d\cf5 \strokec5 ,\cf4 \strokec4  until = Date.fromisoformat\cf5 \strokec5 (\cf4 \strokec4 body.date\cf5 \strokec5 ),\cf4 \strokec4  Date.fromisoformat\cf5 \strokec5 (\cf4 \strokec4 body.repeat_until\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 while\cf4 \strokec4  \cf5 \strokec5 (\cf4 \strokec4 d \cf5 \strokec5 :\cf4 \strokec4 = d + timedelta\cf5 \strokec5 (\cf4 \strokec4 days=\cf7 \strokec7 7\cf5 \strokec5 ))\cf4 \strokec4  <= until\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3             dates.append\cf5 \strokec5 (\cf4 \strokec4 d.isoformat\cf5 \strokec5 ())\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 len\cf5 \strokec5 (\cf4 \strokec4 dates\cf5 \strokec5 )\cf4 \strokec4  > MAX_REPEATS\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 f"Massimo \cf4 \strokec4 \{MAX_REPEATS\}\cf6 \strokec6  turni ripetuti per volta"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     series_id = \cf2 \strokec2 str\cf5 \strokec5 (\cf4 \strokec4 uuid.uuid4\cf5 \strokec5 ())\cf4 \strokec4  \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 len\cf5 \strokec5 (\cf4 \strokec4 dates\cf5 \strokec5 )\cf4 \strokec4  > \cf7 \strokec7 1\cf4 \strokec4  \cf2 \strokec2 else\cf4 \strokec4  \cf2 \strokec2 None\cf4 \cb1 \strokec4 \
\cb3     created\cf5 \strokec5 ,\cf4 \strokec4  skipped = \cf5 \strokec5 [],\cf4 \strokec4  \cf5 \strokec5 []\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 for\cf4 \strokec4  d \cf2 \strokec2 in\cf4 \strokec4  dates\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         doc = \cf5 \strokec5 \{\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 (\cf4 \strokec4 uuid.uuid4\cf5 \strokec5 ()),\cf4 \strokec4  \cf6 \strokec6 "station"\cf5 \strokec5 :\cf4 \strokec4  body.station\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  d\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "start"\cf5 \strokec5 :\cf4 \strokec4  body.start\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "end"\cf5 \strokec5 :\cf4 \strokec4  body.end\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3             \cf6 \strokec6 "leader_id"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 None\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "member_ids"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 [],\cf4 \strokec4  \cf6 \strokec6 "volunteer_ids"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 [],\cf4 \strokec4  \cf6 \strokec6 "series_id"\cf5 \strokec5 :\cf4 \strokec4  series_id\cf5 \strokec5 ,\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 try\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 await\cf4 \strokec4  db.shifts.insert_one\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3             created.append\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 except\cf4 \strokec4  DuplicateKeyError\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3             skipped.append\cf5 \strokec5 (\cf4 \strokec4 d\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  created\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  DUP_MSG\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  ShiftBulkOut\cf5 \strokec5 (\cf4 \strokec4 created=\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 (\cf4 \strokec4 created\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 ),\cf4 \strokec4  skipped_dates=skipped\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  update_shift\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  body\cf5 \strokec5 :\cf4 \strokec4  ShiftIn\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     s = \cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  body.station != s\cf5 \strokec5 [\cf6 \strokec6 "station"\cf5 \strokec5 ]:\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 await\cf4 \strokec4  check_station\cf5 \strokec5 (\cf4 \strokec4 body.station\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     data = \cf5 \strokec5 \{\cf6 \strokec6 "station"\cf5 \strokec5 :\cf4 \strokec4  body.station\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  body.date\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "start"\cf5 \strokec5 :\cf4 \strokec4  body.start\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "end"\cf5 \strokec5 :\cf4 \strokec4  body.end\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 await\cf4 \strokec4  db.shifts.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  data\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  DuplicateKeyError\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  DUP_MSG\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 ([\{\cf4 \strokec4 **s\cf5 \strokec5 ,\cf4 \strokec4  **data\cf5 \strokec5 \}],\cf4 \strokec4  user\cf5 \strokec5 ))[\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .delete\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  delete_shift\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     res = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.delete_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  res.deleted_count\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Turno non trovato"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.reports.delete_many\cf5 \strokec5 (\{\cf6 \strokec6 "shift_id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "ok"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}/join"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  join_shift\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  body\cf5 \strokec5 :\cf4 \strokec4  Optional\cf5 \strokec5 [\cf4 \strokec4 JoinIn\cf5 \strokec5 ]\cf4 \strokec4  = \cf2 \strokec2 None\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     as_role = \cf5 \strokec5 (\cf4 \strokec4 body \cf2 \strokec2 or\cf4 \strokec4  JoinIn\cf5 \strokec5 ())\cf4 \strokec4 .as_role\cb1 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "role"\cf5 \strokec5 ]\cf4 \strokec4  != \cf6 \strokec6 "volunteer"\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 403\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Gli amministratori si assegnano dal pulsante Assegna"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  user.get\cf5 \strokec5 (\cf6 \strokec6 "gender"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 in\cf4 \strokec4  \cf5 \strokec5 (\cf6 \strokec6 "M"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "F"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 or\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  user.get\cf5 \strokec5 (\cf6 \strokec6 "phone"\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Completa il profilo (genere e telefono) prima di iscriverti"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     s = \cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  s\cf5 \strokec5 [\cf6 \strokec6 "date"\cf5 \strokec5 ]\cf4 \strokec4  < today_iso\cf5 \strokec5 ():\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Non \'e8 possibile iscriversi a un turno passato"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  place\cf5 \strokec5 (\cf4 \strokec4 s\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 ,\cf4 \strokec4  as_role\cf5 \strokec5 ,\cf4 \strokec4  enforce_monthly=\cf2 \strokec2 True\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 ([\cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )],\cf4 \strokec4  user\cf5 \strokec5 ))[\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}/assign"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  assign\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  body\cf5 \strokec5 :\cf4 \strokec4  AssignIn\cf5 \strokec5 ,\cf4 \strokec4  admin\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 """Admin places any volunteer (or an admin, incl. themselves). Skips only the monthly limit."""\cf4 \cb1 \strokec4 \
\cb3     s = \cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     target = \cf2 \strokec2 await\cf4 \strokec4  db.users.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  body.user_id\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  target\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Persona non trovata"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  place\cf5 \strokec5 (\cf4 \strokec4 s\cf5 \strokec5 ,\cf4 \strokec4  target\cf5 \strokec5 ,\cf4 \strokec4  body.as_role\cf5 \strokec5 ,\cf4 \strokec4  enforce_monthly=\cf2 \strokec2 False\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 ([\cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )],\cf4 \strokec4  admin\cf5 \strokec5 ))[\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}/leave"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  leave_shift\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  user\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     s = \cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ]\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 in\cf4 \strokec4  s.get\cf5 \strokec5 (\cf6 \strokec6 "volunteer_ids"\cf5 \strokec5 ,\cf4 \strokec4  \cf5 \strokec5 []):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Non sei iscritto a questo turno"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  s\cf5 \strokec5 [\cf6 \strokec6 "date"\cf5 \strokec5 ]\cf4 \strokec4  < today_iso\cf5 \strokec5 ()\cf4 \strokec4  \cf2 \strokec2 and\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "role"\cf5 \strokec5 ]\cf4 \strokec4  != \cf6 \strokec6 "admin"\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Non \'e8 possibile cancellarsi da un turno passato"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  remove_volunteer\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \},\cf4 \strokec4  user\cf5 \strokec5 [\cf6 \strokec6 "id"\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 ([\cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )],\cf4 \strokec4  user\cf5 \strokec5 ))[\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf8 \cb3 \strokec8 @router\cf4 \strokec4 .delete\cf5 \strokec5 (\cf6 \strokec6 "/shifts/\{shift_id\}/volunteers/\{user_id\}"\cf5 \strokec5 ,\cf4 \strokec4  response_model=ShiftOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  admin_remove\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  user_id\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  admin\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  remove_volunteer\cf5 \strokec5 (\{\cf6 \strokec6 "id"\cf5 \strokec5 :\cf4 \strokec4  shift_id\cf5 \strokec5 \},\cf4 \strokec4  user_id\cf5 \strokec5 ):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf7 \strokec7 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Volontario non iscritto a questo turno"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 (\cf2 \strokec2 await\cf4 \strokec4  serialize\cf5 \strokec5 ([\cf2 \strokec2 await\cf4 \strokec4  load\cf5 \strokec5 (\cf4 \strokec4 shift_id\cf5 \strokec5 )],\cf4 \strokec4  admin\cf5 \strokec5 ))[\cf7 \strokec7 0\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
}