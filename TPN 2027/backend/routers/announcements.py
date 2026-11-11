{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red51\green95\blue50;\red249\green249\blue249;\red157\green88\blue173;
\red16\green16\blue16;\red187\green187\blue187;\red212\green212\blue212;\red80\green173\blue77;\red70\green137\blue204;
\red191\green91\blue43;}
{\*\expandedcolortbl;;\cssrgb\c25490\c43922\c25490;\cssrgb\c98039\c98039\c98039;\cssrgb\c68235\c44314\c73333;
\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;\cssrgb\c86275\c86275\c86275;\cssrgb\c37255\c72157\c37255;\cssrgb\c33725\c61176\c83922;
\cssrgb\c80000\c43922\c21961;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
1\cf4 \cb5 \outl0\strokewidth0 \strokec4 import\cf6 \strokec6  uuid\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb5 \strokec4 from\cf6 \strokec6  datetime \cf4 \strokec4 import\cf6 \strokec6  datetime\cf7 \strokec7 ,\cf6 \strokec6  timezone\cb1 \
\
\cf4 \cb5 \strokec4 from\cf6 \strokec6  fastapi \cf4 \strokec4 import\cf6 \strokec6  APIRouter\cf7 \strokec7 ,\cf6 \strokec6  Depends\cf7 \strokec7 ,\cf6 \strokec6  HTTPException\cb1 \
\
\cf4 \cb5 \strokec4 from\cf6 \strokec6  lib.auth \cf4 \strokec4 import\cf6 \strokec6  current_user\cf7 \strokec7 ,\cf6 \strokec6  require_admin\cb1 \
\cf4 \cb5 \strokec4 from\cf6 \strokec6  lib.db \cf4 \strokec4 import\cf6 \strokec6  db\cb1 \
\cf4 \cb5 \strokec4 from\cf6 \strokec6  models.schemas \cf4 \strokec4 import\cf6 \strokec6  Announcement\cf7 \strokec7 ,\cf6 \strokec6  AnnouncementIn\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf6 \cb5 router = APIRouter\cf7 \strokec7 ()\cf6 \cb1 \strokec6 \
\
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb5 \strokec4 def\cf6 \strokec6  to_out\cf7 \strokec7 (\cf6 \strokec6 d\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 dict\cf7 \strokec7 )\cf6 \strokec6  -> Announcement\cf7 \strokec7 :\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb5     ts = d\cf7 \strokec7 [\cf8 \strokec8 "created_at"\cf7 \strokec7 ]\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 if\cf6 \strokec6  ts.tzinfo \cf4 \strokec4 is\cf6 \strokec6  \cf4 \strokec4 None\cf7 \strokec7 :\cf6 \cb1 \strokec6 \
\cb5         ts = ts.replace\cf7 \strokec7 (\cf6 \strokec6 tzinfo=timezone.utc\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 return\cf6 \strokec6  Announcement\cf7 \strokec7 (\cf6 \strokec6 **\cf7 \strokec7 \{\cf6 \strokec6 **d\cf7 \strokec7 ,\cf6 \strokec6  \cf8 \strokec8 "created_at"\cf7 \strokec7 :\cf6 \strokec6  ts\cf7 \strokec7 \})\cf6 \cb1 \strokec6 \
\
\
\pard\pardeftab720\partightenfactor0
\cf9 \cb5 \strokec9 @router\cf6 \strokec6 .get\cf7 \strokec7 (\cf8 \strokec8 "/announcements"\cf7 \strokec7 ,\cf6 \strokec6  response_model=\cf4 \strokec4 list\cf7 \strokec7 [\cf6 \strokec6 Announcement\cf7 \strokec7 ])\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb5 \strokec4 async\cf6 \strokec6  \cf4 \strokec4 def\cf6 \strokec6  list_announcements\cf7 \strokec7 (\cf4 \strokec4 _\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 dict\cf6 \strokec6  = Depends\cf7 \strokec7 (\cf6 \strokec6 current_user\cf7 \strokec7 )):\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb5     docs = \cf4 \strokec4 await\cf6 \strokec6  db.announcements.find\cf7 \strokec7 (\{\},\cf6 \strokec6  \cf7 \strokec7 \{\cf8 \strokec8 "_id"\cf7 \strokec7 :\cf6 \strokec6  \cf10 \strokec10 0\cf7 \strokec7 \})\cf6 \strokec6 .sort\cf7 \strokec7 ([(\cf8 \strokec8 "pinned"\cf7 \strokec7 ,\cf6 \strokec6  \cf10 \strokec10 -1\cf7 \strokec7 ),\cf6 \strokec6  \cf7 \strokec7 (\cf8 \strokec8 "created_at"\cf7 \strokec7 ,\cf6 \strokec6  \cf10 \strokec10 -1\cf7 \strokec7 )])\cf6 \strokec6 .to_list\cf7 \strokec7 (\cf10 \strokec10 500\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 return\cf6 \strokec6  \cf7 \strokec7 [\cf6 \strokec6 to_out\cf7 \strokec7 (\cf6 \strokec6 d\cf7 \strokec7 )\cf6 \strokec6  \cf4 \strokec4 for\cf6 \strokec6  d \cf4 \strokec4 in\cf6 \strokec6  docs\cf7 \strokec7 ]\cf6 \cb1 \strokec6 \
\
\
\pard\pardeftab720\partightenfactor0
\cf9 \cb5 \strokec9 @router\cf6 \strokec6 .post\cf7 \strokec7 (\cf8 \strokec8 "/announcements"\cf7 \strokec7 ,\cf6 \strokec6  response_model=Announcement\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb5 \strokec4 async\cf6 \strokec6  \cf4 \strokec4 def\cf6 \strokec6  create_announcement\cf7 \strokec7 (\cf6 \strokec6 body\cf7 \strokec7 :\cf6 \strokec6  AnnouncementIn\cf7 \strokec7 ,\cf6 \strokec6  admin\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 dict\cf6 \strokec6  = Depends\cf7 \strokec7 (\cf6 \strokec6 require_admin\cf7 \strokec7 )):\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb5     author = \cf8 \strokec8 f"\cf6 \strokec6 \{admin.get('first_name', '')\}\cf8 \strokec8  \cf6 \strokec6 \{admin.get('last_name', '')\}\cf8 \strokec8 "\cf6 \strokec6 .strip\cf7 \strokec7 ()\cf6 \strokec6  \cf4 \strokec4 or\cf6 \strokec6  \cf8 \strokec8 "Amministratore"\cf6 \cb1 \strokec6 \
\cb5     doc = \cf7 \strokec7 \{\cf8 \strokec8 "id"\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 str\cf7 \strokec7 (\cf6 \strokec6 uuid.uuid4\cf7 \strokec7 ()),\cf6 \strokec6  \cf8 \strokec8 "title"\cf7 \strokec7 :\cf6 \strokec6  body.title.strip\cf7 \strokec7 (),\cf6 \strokec6  \cf8 \strokec8 "body"\cf7 \strokec7 :\cf6 \strokec6  body.body.strip\cf7 \strokec7 (),\cf6 \cb1 \strokec6 \
\cb5            \cf8 \strokec8 "pinned"\cf7 \strokec7 :\cf6 \strokec6  body.pinned\cf7 \strokec7 ,\cf6 \strokec6  \cf8 \strokec8 "author_name"\cf7 \strokec7 :\cf6 \strokec6  author\cf7 \strokec7 ,\cf6 \strokec6  \cf8 \strokec8 "created_at"\cf7 \strokec7 :\cf6 \strokec6  datetime.now\cf7 \strokec7 (\cf6 \strokec6 timezone.utc\cf7 \strokec7 )\}\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 await\cf6 \strokec6  db.announcements.insert_one\cf7 \strokec7 (\cf6 \strokec6 doc\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 return\cf6 \strokec6  to_out\cf7 \strokec7 (\cf6 \strokec6 doc\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\
\
\pard\pardeftab720\partightenfactor0
\cf9 \cb5 \strokec9 @router\cf6 \strokec6 .delete\cf7 \strokec7 (\cf8 \strokec8 "/announcements/\{aid\}"\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb5 \strokec4 async\cf6 \strokec6  \cf4 \strokec4 def\cf6 \strokec6  delete_announcement\cf7 \strokec7 (\cf6 \strokec6 aid\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 str\cf7 \strokec7 ,\cf6 \strokec6  \cf4 \strokec4 _\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 dict\cf6 \strokec6  = Depends\cf7 \strokec7 (\cf6 \strokec6 require_admin\cf7 \strokec7 )):\cf6 \cb1 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb5     res = \cf4 \strokec4 await\cf6 \strokec6  db.announcements.delete_one\cf7 \strokec7 (\{\cf8 \strokec8 "id"\cf7 \strokec7 :\cf6 \strokec6  aid\cf7 \strokec7 \})\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 if\cf6 \strokec6  \cf4 \strokec4 not\cf6 \strokec6  res.deleted_count\cf7 \strokec7 :\cf6 \cb1 \strokec6 \
\cb5         \cf4 \strokec4 raise\cf6 \strokec6  HTTPException\cf7 \strokec7 (\cf10 \strokec10 404\cf7 \strokec7 ,\cf6 \strokec6  \cf8 \strokec8 "Avviso non trovato"\cf7 \strokec7 )\cf6 \cb1 \strokec6 \
\cb5     \cf4 \strokec4 return\cf6 \strokec6  \cf7 \strokec7 \{\cf8 \strokec8 "ok"\cf7 \strokec7 :\cf6 \strokec6  \cf4 \strokec4 True\cf7 \strokec7 \}\cf6 \cb1 \strokec6 \
\
}