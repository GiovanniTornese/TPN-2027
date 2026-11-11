{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red51\green95\blue50;\red249\green249\blue249;\red45\green45\blue45;
\red103\green38\blue120;\red0\green0\blue0;\red129\green129\blue129;\red133\green40\blue2;}
{\*\expandedcolortbl;;\cssrgb\c25490\c43922\c25490;\cssrgb\c98039\c98039\c98039;\cssrgb\c23137\c23137\c23137;
\cssrgb\c48627\c23137\c54510;\cssrgb\c0\c0\c0;\cssrgb\c57647\c57647\c57647;\cssrgb\c60000\c21961\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 """Shared Mongo handle \'97 import `client`/`db` from here (server.py, routers, seed.py)."""\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  logging\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  pathlib \cf5 \strokec5 import\cf4 \strokec4  Path\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  dotenv \cf5 \strokec5 import\cf4 \strokec4  load_dotenv\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  motor.motor_asyncio \cf5 \strokec5 import\cf4 \strokec4  AsyncIOMotorClient\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  pymongo \cf5 \strokec5 import\cf4 \strokec4  ASCENDING\strokec6 ,\strokec4  DESCENDING\strokec6 ,\strokec4  IndexModel\cb1 \
\
\cb3 load_dotenv\strokec6 (\strokec4 Path\strokec6 (\strokec4 __file__\strokec6 )\strokec4 .parent.parent / \cf2 \strokec2 ".env"\cf4 \strokec6 )\cb1 \strokec4 \
\
\cb3 mongo_url = os.environ\strokec6 [\cf2 \strokec2 "MONGO_URL"\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3 client = AsyncIOMotorClient\strokec6 (\strokec4 mongo_url\strokec6 )\cb1 \strokec4 \
\cb3 db = client\strokec6 [\strokec4 os.environ\strokec6 [\cf2 \strokec2 "DB_NAME"\cf4 \strokec6 ]]\cb1 \strokec4 \
\
\cb3 logger = logging.getLogger\strokec6 (\cf5 \strokec5 __name__\cf4 \strokec6 )\cb1 \strokec4 \
\
\cf7 \cb3 \strokec7 # One entry per collection: every field a route filters, sorts, or dedupes on. Applied by ensure_indexes() at startup.\cf4 \cb1 \strokec4 \
\cb3 INDEXES\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec6 [\cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  \cf5 \strokec5 list\cf4 \strokec6 [\strokec4 IndexModel\strokec6 ]]\strokec4  = \strokec6 \{\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "users"\cf4 \strokec6 :\strokec4  \strokec6 [\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "email"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "email"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "role"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "last_name"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "role_name"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 ],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "shifts"\cf4 \strokec6 :\strokec4  \strokec6 [\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "station"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "date"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "start"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "station_date_start"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "date"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "start"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "date_start"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "date"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "volunteer_date"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "leader_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "date"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "leader_date"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 ],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "stations"\cf4 \strokec6 :\strokec4  \strokec6 [\strokec4 IndexModel\strokec6 ([(\cf2 \strokec2 "key"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "key"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 )],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "reports"\cf4 \strokec6 :\strokec4  \strokec6 [\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "shift_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "user_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "shift_user"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "user_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "updated_at"\cf4 \strokec6 ,\strokec4  DESCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "user_updated"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 ],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "reminders_sent"\cf4 \strokec6 :\strokec4  \strokec6 [\strokec4 IndexModel\strokec6 ([(\cf2 \strokec2 "user_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "date"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "user_date"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 )],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "cron_runs"\cf4 \strokec6 :\strokec4  \strokec6 [\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "run_id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "run_id"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "at"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "ttl"\cf4 \strokec6 ,\strokec4  expireAfterSeconds=\cf8 \strokec8 30\cf4 \strokec4  * \cf8 \strokec8 86400\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 ],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "settings"\cf4 \strokec6 :\strokec4  \strokec6 [\strokec4 IndexModel\strokec6 ([(\cf2 \strokec2 "key"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "key"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 )],\cb1 \strokec4 \
\cb3     \cf2 \strokec2 "announcements"\cf4 \strokec6 :\strokec4  \strokec6 [\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  ASCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "id"\cf4 \strokec6 ,\strokec4  unique=\cf5 \strokec5 True\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3         IndexModel\strokec6 ([(\cf2 \strokec2 "pinned"\cf4 \strokec6 ,\strokec4  DESCENDING\strokec6 ),\strokec4  \strokec6 (\cf2 \strokec2 "created_at"\cf4 \strokec6 ,\strokec4  DESCENDING\strokec6 )],\strokec4  name=\cf2 \strokec2 "pinned_created"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 ],\cb1 \strokec4 \
\cb3 \strokec6 \}\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  ensure_indexes\strokec6 ()\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  collection\strokec6 ,\strokec4  models \cf5 \strokec5 in\cf4 \strokec4  INDEXES.items\strokec6 ():\cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  model \cf5 \strokec5 in\cf4 \strokec4  models\strokec6 :\strokec4   \cf7 \strokec7 # one at a time so a bad spec skips only itself\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3                 \cf5 \strokec5 await\cf4 \strokec4  db\strokec6 [\strokec4 collection\strokec6 ]\strokec4 .create_indexes\strokec6 ([\strokec4 model\strokec6 ])\cb1 \strokec4 \
\cb3             \cf5 \strokec5 except\cf4 \strokec4  Exception \cf5 \strokec5 as\cf4 \strokec4  exc\strokec6 :\strokec4   \cf7 \strokec7 # never block boot on an index; the log line names what to fix\cf4 \cb1 \strokec4 \
\cb3                 logger.error\strokec6 (\cf2 \strokec2 "ensure_indexes(%s.%s): %s"\cf4 \strokec6 ,\strokec4  collection\strokec6 ,\strokec4  model.document\strokec6 [\cf2 \strokec2 "name"\cf4 \strokec6 ],\strokec4  exc\strokec6 )\cb1 \strokec4 \
\
}