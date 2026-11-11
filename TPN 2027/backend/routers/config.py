{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red157\green88\blue173;\red16\green16\blue16;\red187\green187\blue187;
\red212\green212\blue212;\red80\green173\blue77;\red70\green137\blue204;\red191\green91\blue43;}
{\*\expandedcolortbl;;\cssrgb\c68235\c44314\c73333;\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;
\cssrgb\c86275\c86275\c86275;\cssrgb\c37255\c72157\c37255;\cssrgb\c33725\c61176\c83922;\cssrgb\c80000\c43922\c21961;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf4 \strokec4  uuid\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  fastapi \cf2 \strokec2 import\cf4 \strokec4  APIRouter\cf5 \strokec5 ,\cf4 \strokec4  Depends\cf5 \strokec5 ,\cf4 \strokec4  HTTPException\cb1 \
\
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.auth \cf2 \strokec2 import\cf4 \strokec4  current_user\cf5 \strokec5 ,\cf4 \strokec4  require_admin\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.dates \cf2 \strokec2 import\cf4 \strokec4  today_iso\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  lib.db \cf2 \strokec2 import\cf4 \strokec4  db\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  models.schemas \cf2 \strokec2 import\cf4 \strokec4  SlotsIn\cf5 \strokec5 ,\cf4 \strokec4  SlotsOut\cf5 \strokec5 ,\cf4 \strokec4  Station\cf5 \strokec5 ,\cf4 \strokec4  StationIn\cf5 \strokec5 ,\cf4 \strokec4  TodayOut\cb1 \
\
\cb3 router = APIRouter\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3 PALETTE = \cf5 \strokec5 [\cf6 \strokec6 "emerald"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "indigo"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "amber"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "rose"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "cyan"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "violet"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "lime"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "orange"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "fuchsia"\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "teal"\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/today"\cf5 \strokec5 ,\cf4 \strokec4  response_model=TodayOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  today\cf5 \strokec5 ():\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  TodayOut\cf5 \strokec5 (\cf4 \strokec4 today=today_iso\cf5 \strokec5 ())\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/stations"\cf5 \strokec5 ,\cf4 \strokec4  response_model=\cf2 \strokec2 list\cf5 \strokec5 [\cf4 \strokec4 Station\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  list_stations\cf5 \strokec5 (\cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 """Active and archived stations (archived ones are kept so past shifts still show their name)."""\cf4 \cb1 \strokec4 \
\cb3     docs = \cf2 \strokec2 await\cf4 \strokec4  db.stations.find\cf5 \strokec5 (\{\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 0\cf5 \strokec5 \})\cf4 \strokec4 .sort\cf5 \strokec5 (\cf6 \strokec6 "order"\cf5 \strokec5 ,\cf4 \strokec4  \cf8 \strokec8 1\cf5 \strokec5 )\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf8 \strokec8 100\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 [\cf4 \strokec4 Station\cf5 \strokec5 (\cf4 \strokec4 **d\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  d \cf2 \strokec2 in\cf4 \strokec4  docs\cf5 \strokec5 ]\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .post\cf5 \strokec5 (\cf6 \strokec6 "/stations"\cf5 \strokec5 ,\cf4 \strokec4  response_model=Station\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  create_station\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  StationIn\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     active = \cf2 \strokec2 await\cf4 \strokec4  db.stations.find\cf5 \strokec5 (\{\cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$ne"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 0\cf5 \strokec5 \})\cf4 \strokec4 .to_list\cf5 \strokec5 (\cf8 \strokec8 100\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     used = \cf5 \strokec5 \{\cf4 \strokec4 s.get\cf5 \strokec5 (\cf6 \strokec6 "color"\cf5 \strokec5 )\cf4 \strokec4  \cf2 \strokec2 for\cf4 \strokec4  s \cf2 \strokec2 in\cf4 \strokec4  active\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3     color = \cf2 \strokec2 next\cf5 \strokec5 ((\cf4 \strokec4 c \cf2 \strokec2 for\cf4 \strokec4  c \cf2 \strokec2 in\cf4 \strokec4  PALETTE \cf2 \strokec2 if\cf4 \strokec4  c \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 in\cf4 \strokec4  used\cf5 \strokec5 ),\cf4 \strokec4  PALETTE\cf5 \strokec5 [\cf2 \strokec2 len\cf5 \strokec5 (\cf4 \strokec4 active\cf5 \strokec5 )\cf4 \strokec4  % \cf2 \strokec2 len\cf5 \strokec5 (\cf4 \strokec4 PALETTE\cf5 \strokec5 )])\cf4 \cb1 \strokec4 \
\cb3     count = \cf2 \strokec2 await\cf4 \strokec4  db.stations.count_documents\cf5 \strokec5 (\{\})\cf4 \cb1 \strokec4 \
\cb3     doc = \cf5 \strokec5 \{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  uuid.uuid4\cf5 \strokec5 ()\cf4 \strokec4 .\cf2 \strokec2 hex\cf5 \strokec5 [:\cf8 \strokec8 8\cf5 \strokec5 ],\cf4 \strokec4  \cf6 \strokec6 "name"\cf5 \strokec5 :\cf4 \strokec4  body.name.strip\cf5 \strokec5 (),\cf4 \strokec4  \cf6 \strokec6 "color"\cf5 \strokec5 :\cf4 \strokec4  color\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 False\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "order"\cf5 \strokec5 :\cf4 \strokec4  count\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.stations.insert_one\cf5 \strokec5 (\cf4 \strokec4 doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  Station\cf5 \strokec5 (\cf4 \strokec4 **doc\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/stations/\{key\}"\cf5 \strokec5 ,\cf4 \strokec4  response_model=Station\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  rename_station\cf5 \strokec5 (\cf4 \strokec4 key\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  body\cf5 \strokec5 :\cf4 \strokec4  StationIn\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     name = body.name.strip\cf5 \strokec5 ()\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  name\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf8 \strokec8 422\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Nome obbligatorio"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     res = \cf2 \strokec2 await\cf4 \strokec4  db.stations.find_one_and_update\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  key\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "name"\cf5 \strokec5 :\cf4 \strokec4  name\cf5 \strokec5 \}\},\cf4 \strokec4  projection=\cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 0\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  res\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf8 \strokec8 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Postazione non trovata"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  Station\cf5 \strokec5 (\cf4 \strokec4 **\cf5 \strokec5 \{\cf4 \strokec4 **res\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "name"\cf5 \strokec5 :\cf4 \strokec4  name\cf5 \strokec5 \})\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .delete\cf5 \strokec5 (\cf6 \strokec6 "/stations/\{key\}"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  delete_station\cf5 \strokec5 (\cf4 \strokec4 key\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 str\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 not\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.stations.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  key\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$ne"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\}):\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf8 \strokec8 404\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Postazione non trovata"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     future = \cf2 \strokec2 await\cf4 \strokec4  db.shifts.count_documents\cf5 \strokec5 (\{\cf6 \strokec6 "station"\cf5 \strokec5 :\cf4 \strokec4  key\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "date"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$gte"\cf5 \strokec5 :\cf4 \strokec4  today_iso\cf5 \strokec5 ()\}\})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  future\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf8 \strokec8 409\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 f"La postazione ha ancora \cf4 \strokec4 \{future\}\cf6 \strokec6  turni futuri: spostali o eliminali prima"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf4 \strokec4  \cf2 \strokec2 await\cf4 \strokec4  db.stations.count_documents\cf5 \strokec5 (\{\cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$ne"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\})\cf4 \strokec4  <= \cf8 \strokec8 1\cf5 \strokec5 :\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 raise\cf4 \strokec4  HTTPException\cf5 \strokec5 (\cf8 \strokec8 400\cf5 \strokec5 ,\cf4 \strokec4  \cf6 \strokec6 "Deve restare almeno una postazione"\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.stations.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  key\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "archived"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\})\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "ok"\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 True\cf5 \strokec5 \}\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .get\cf5 \strokec5 (\cf6 \strokec6 "/settings/slots"\cf5 \strokec5 ,\cf4 \strokec4  response_model=SlotsOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  get_slots\cf5 \strokec5 (\cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 current_user\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     doc = \cf2 \strokec2 await\cf4 \strokec4  db.settings.find_one\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "slots"\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "_id"\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 0\cf5 \strokec5 \})\cf4 \strokec4  \cf2 \strokec2 or\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "slots"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 []\}\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  SlotsOut\cf5 \strokec5 (\cf4 \strokec4 slots=doc\cf5 \strokec5 [\cf6 \strokec6 "slots"\cf5 \strokec5 ])\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @router\cf4 \strokec4 .put\cf5 \strokec5 (\cf6 \strokec6 "/settings/slots"\cf5 \strokec5 ,\cf4 \strokec4  response_model=SlotsOut\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 async\cf4 \strokec4  \cf2 \strokec2 def\cf4 \strokec4  set_slots\cf5 \strokec5 (\cf4 \strokec4 body\cf5 \strokec5 :\cf4 \strokec4  SlotsIn\cf5 \strokec5 ,\cf4 \strokec4  \cf2 \strokec2 _\cf5 \strokec5 :\cf4 \strokec4  \cf2 \strokec2 dict\cf4 \strokec4  = Depends\cf5 \strokec5 (\cf4 \strokec4 require_admin\cf5 \strokec5 )):\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 await\cf4 \strokec4  db.settings.update_one\cf5 \strokec5 (\{\cf6 \strokec6 "key"\cf5 \strokec5 :\cf4 \strokec4  \cf6 \strokec6 "slots"\cf5 \strokec5 \},\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "$set"\cf5 \strokec5 :\cf4 \strokec4  \cf5 \strokec5 \{\cf6 \strokec6 "slots"\cf5 \strokec5 :\cf4 \strokec4  body.slots\cf5 \strokec5 \}\},\cf4 \strokec4  upsert=\cf2 \strokec2 True\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  SlotsOut\cf5 \strokec5 (\cf4 \strokec4 slots=body.slots\cf5 \strokec5 )\cf4 \cb1 \strokec4 \
\
}