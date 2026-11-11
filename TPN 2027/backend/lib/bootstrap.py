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
\outl0\strokewidth0 \strokec2 """Idempotent startup seed: the two admin accounts (once), 3 stations, default 2h slots, shift-shape migration."""\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  uuid\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  datetime \cf5 \strokec5 import\cf4 \strokec4  datetime\strokec6 ,\strokec4  timezone\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.auth \cf5 \strokec5 import\cf4 \strokec4  hash_pw\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.db \cf5 \strokec5 import\cf4 \strokec4  db\cb1 \
\
\cb3 DEFAULT_STATIONS = \strokec6 \{\cf2 \strokec2 "a"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "Postazione A"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "b"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "Postazione B"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "c"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "Postazione C"\cf4 \strokec6 \}\cb1 \strokec4 \
\cb3 DEFAULT_SLOTS = \strokec6 [\cf2 \strokec2 "08:00"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "10:00"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "12:00"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "14:00"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "16:00"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "18:00"\cf4 \strokec6 ]\cb1 \strokec4 \
\
\cf7 \cb3 \strokec7 # Seeded only once (settings flag), so later email/password changes made in-app are never overwritten.\cf4 \cb1 \strokec4 \
\cb3 ADMINS = \strokec6 [\cb1 \strokec4 \
\cb3     \strokec6 (\cf2 \strokec2 "gnnitornese@gmail.com"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Giovanni"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Tornese"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3     \strokec6 (\cf2 \strokec2 "andrea.volpicelli@tpn2027.it"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Andrea"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Volpicelli"\cf4 \strokec6 ),\cb1 \strokec4 \
\cb3 \strokec6 ]\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  bootstrap\strokec6 ()\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 await\cf4 \strokec4  db.settings.find_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admins_seeded_v2"\cf4 \strokec6 \}):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 await\cf4 \strokec4  db.users.delete_many\strokec6 (\{\cf2 \strokec2 "email"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admin@associazione.it"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "role"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admin"\cf4 \strokec6 \})\cb1 \strokec4 \
\cb3         password = os.environ.get\strokec6 (\cf2 \strokec2 "ADMIN_PASSWORD"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Admin123!"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  email\strokec6 ,\strokec4  first\strokec6 ,\strokec4  last \cf5 \strokec5 in\cf4 \strokec4  ADMINS\strokec6 :\cb1 \strokec4 \
\cb3             existing = \cf5 \strokec5 await\cf4 \strokec4  db.users.find_one\strokec6 (\{\cf2 \strokec2 "email"\cf4 \strokec6 :\strokec4  email\strokec6 \})\cb1 \strokec4 \
\cb3             \cf5 \strokec5 if\cf4 \strokec4  existing\strokec6 :\cb1 \strokec4 \
\cb3                 \cf5 \strokec5 await\cf4 \strokec4  db.users.update_one\strokec6 (\{\cf2 \strokec2 "email"\cf4 \strokec6 :\strokec4  email\strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "$set"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "role"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admin"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "first_name"\cf4 \strokec6 :\strokec4  first\strokec6 ,\strokec4  \cf2 \strokec2 "last_name"\cf4 \strokec6 :\strokec4  last\strokec6 \}\})\cb1 \strokec4 \
\cb3                 \cf5 \strokec5 continue\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 await\cf4 \strokec4  db.users.insert_one\strokec6 (\{\cb1 \strokec4 \
\cb3                 \cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 (\strokec4 uuid.uuid4\strokec6 ()),\strokec4  \cf2 \strokec2 "email"\cf4 \strokec6 :\strokec4  email\strokec6 ,\strokec4  \cf2 \strokec2 "password_hash"\cf4 \strokec6 :\strokec4  hash_pw\strokec6 (\strokec4 password\strokec6 ),\cb1 \strokec4 \
\cb3                 \cf2 \strokec2 "role"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admin"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "first_name"\cf4 \strokec6 :\strokec4  first\strokec6 ,\strokec4  \cf2 \strokec2 "last_name"\cf4 \strokec6 :\strokec4  last\strokec6 ,\strokec4  \cf2 \strokec2 "phone"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 ""\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3                 \cf2 \strokec2 "gender"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "M"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "is_team_leader"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 False\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "created_at"\cf4 \strokec6 :\strokec4  datetime.now\strokec6 (\strokec4 timezone.utc\strokec6 ),\cb1 \strokec4 \
\cb3             \strokec6 \})\cb1 \strokec4 \
\cb3         \cf5 \strokec5 await\cf4 \strokec4  db.settings.insert_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "admins_seeded_v2"\cf4 \strokec6 \})\cb1 \strokec4 \
\
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 await\cf4 \strokec4  db.settings.find_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "stations_seeded"\cf4 \strokec6 \}):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  i\strokec6 ,\strokec4  \strokec6 (\strokec4 key\strokec6 ,\strokec4  name\strokec6 )\strokec4  \cf5 \strokec5 in\cf4 \strokec4  \cf5 \strokec5 enumerate\cf4 \strokec6 (\strokec4 DEFAULT_STATIONS.items\strokec6 ()):\cb1 \strokec4 \
\cb3             \cf5 \strokec5 await\cf4 \strokec4  db.stations.update_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  key\strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "$setOnInsert"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  key\strokec6 ,\strokec4  \cf2 \strokec2 "name"\cf4 \strokec6 :\strokec4  name\strokec6 \}\},\strokec4  upsert=\cf5 \strokec5 True\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 await\cf4 \strokec4  db.settings.insert_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "stations_seeded"\cf4 \strokec6 \})\cb1 \strokec4 \
\cb3     \cf7 \strokec7 # Dynamic stations: make sure the original three have color/order/archived fields.\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  i\strokec6 ,\strokec4  \strokec6 (\strokec4 key\strokec6 ,\strokec4  color\strokec6 )\strokec4  \cf5 \strokec5 in\cf4 \strokec4  \cf5 \strokec5 enumerate\cf4 \strokec6 (\{\cf2 \strokec2 "a"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "emerald"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "b"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "indigo"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "c"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "amber"\cf4 \strokec6 \}\strokec4 .items\strokec6 ()):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 await\cf4 \strokec4  db.stations.update_one\strokec6 (\{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  key\strokec6 ,\strokec4  \cf2 \strokec2 "color"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$exists"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 False\cf4 \strokec6 \}\},\cb1 \strokec4 \
\cb3                                      \strokec6 \{\cf2 \strokec2 "$set"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "color"\cf4 \strokec6 :\strokec4  color\strokec6 ,\strokec4  \cf2 \strokec2 "order"\cf4 \strokec6 :\strokec4  i\strokec6 ,\strokec4  \cf2 \strokec2 "archived"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 False\cf4 \strokec6 \}\})\cb1 \strokec4 \
\cb3     \cf5 \strokec5 await\cf4 \strokec4  db.settings.update_one\strokec6 (\cb1 \strokec4 \
\cb3         \strokec6 \{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "slots"\cf4 \strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "$setOnInsert"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "key"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 "slots"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "slots"\cf4 \strokec6 :\strokec4  DEFAULT_SLOTS\strokec6 \}\},\strokec4  upsert=\cf5 \strokec5 True\cf4 \cb1 \strokec4 \
\cb3     \strokec6 )\cb1 \strokec4 \
\cb3     \cf7 \strokec7 # Migrate shifts from the old men/women shape to leader + members.\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  db.shifts.find\strokec6 (\{\cf2 \strokec2 "member_ids"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "$exists"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 False\cf4 \strokec6 \}\}):\cb1 \strokec4 \
\cb3         ids = s.get\strokec6 (\cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 ,\strokec4  \strokec6 [])[:\cf8 \strokec8 2\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3         \cf5 \strokec5 await\cf4 \strokec4  db.shifts.update_one\strokec6 (\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "_id"\cf4 \strokec6 :\strokec4  s\strokec6 [\cf2 \strokec2 "_id"\cf4 \strokec6 ]\},\cb1 \strokec4 \
\cb3             \strokec6 \{\cf2 \strokec2 "$set"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "leader_id"\cf4 \strokec6 :\strokec4  \cf5 \strokec5 None\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "member_ids"\cf4 \strokec6 :\strokec4  ids\strokec6 ,\strokec4  \cf2 \strokec2 "volunteer_ids"\cf4 \strokec6 :\strokec4  ids\strokec6 \},\strokec4  \cf2 \strokec2 "$unset"\cf4 \strokec6 :\strokec4  \strokec6 \{\cf2 \strokec2 "men"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 ""\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "women"\cf4 \strokec6 :\strokec4  \cf2 \strokec2 ""\cf4 \strokec6 \}\},\cb1 \strokec4 \
\cb3         \strokec6 )\cb1 \strokec4 \
\
}