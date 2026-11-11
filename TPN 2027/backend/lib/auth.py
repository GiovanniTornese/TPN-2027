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
\outl0\strokewidth0 \strokec2 """Cookie-session auth: JWT in an httpOnly cookie, user + role re-read from Mongo on every request."""\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  datetime \cf5 \strokec5 import\cf4 \strokec4  datetime\strokec6 ,\strokec4  timedelta\strokec6 ,\strokec4  timezone\cb1 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  jwt\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  fastapi \cf5 \strokec5 import\cf4 \strokec4  Depends\strokec6 ,\strokec4  HTTPException\strokec6 ,\strokec4  Request\strokec6 ,\strokec4  Response\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  passlib.\cf5 \strokec5 hash\cf4 \strokec4  \cf5 \strokec5 import\cf4 \strokec4  pbkdf2_sha256\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.db \cf5 \strokec5 import\cf4 \strokec4  db\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 COOKIE = \cf2 \strokec2 "session"\cf4 \cb1 \strokec4 \
\cb3 MAX_AGE = \cf7 \strokec7 7\cf4 \strokec4  * \cf7 \strokec7 24\cf4 \strokec4  * \cf7 \strokec7 3600\cf4 \cb1 \strokec4 \
\cb3 SECRET = os.environ\strokec6 [\cf2 \strokec2 "JWT_SECRET"\cf4 \strokec6 ]\cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 def\cf4 \strokec4  hash_pw\strokec6 (\strokec4 pw\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 str\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf5 \strokec5 return\cf4 \strokec4  pbkdf2_sha256.\cf5 \strokec5 hash\cf4 \strokec6 (\strokec4 pw\strokec6 )\cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 def\cf4 \strokec4  verify_pw\strokec6 (\strokec4 pw\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  hashed\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 bool\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  pbkdf2_sha256.verify\strokec6 (\strokec4 pw\strokec6 ,\strokec4  hashed\strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  Exception\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 def\cf4 \strokec4  set_session\strokec6 (\strokec4 response\strokec6 :\strokec4  Response\strokec6 ,\strokec4  user_id\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     exp = datetime.now\strokec6 (\strokec4 timezone.utc\strokec6 )\strokec4  + timedelta\strokec6 (\strokec4 seconds=MAX_AGE\strokec6 )\cb1 \strokec4 \
\cb3     token = jwt.encode\strokec6 (\{\cf2 \strokec2 "sub"\cf4 \strokec6 :\strokec4  user_id\strokec6 ,\strokec4  \cf2 \strokec2 "exp"\cf4 \strokec6 :\strokec4  exp\strokec6 \},\strokec4  SECRET\strokec6 ,\strokec4  algorithm=\cf2 \strokec2 "HS256"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     response.set_cookie\strokec6 (\strokec4 COOKIE\strokec6 ,\strokec4  token\strokec6 ,\strokec4  httponly=\cf5 \strokec5 True\cf4 \strokec6 ,\strokec4  samesite=\cf2 \strokec2 "lax"\cf4 \strokec6 ,\strokec4  max_age=MAX_AGE\strokec6 ,\strokec4  path=\cf2 \strokec2 "/"\cf4 \strokec6 )\cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 def\cf4 \strokec4  clear_session\strokec6 (\strokec4 response\strokec6 :\strokec4  Response\strokec6 )\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     response.delete_cookie\strokec6 (\strokec4 COOKIE\strokec6 ,\strokec4  path=\cf2 \strokec2 "/"\cf4 \strokec6 )\cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  current_user\strokec6 (\strokec4 request\strokec6 :\strokec4  Request\strokec6 )\strokec4  -> \cf5 \strokec5 dict\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     token = request.cookies.get\strokec6 (\strokec4 COOKIE\strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  token\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 401\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Non autenticato"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         sub = jwt.decode\strokec6 (\strokec4 token\strokec6 ,\strokec4  SECRET\strokec6 ,\strokec4  algorithms=\strokec6 [\cf2 \strokec2 "HS256"\cf4 \strokec6 ])[\cf2 \strokec2 "sub"\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  jwt.PyJWTError\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 401\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Sessione non valida"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     user = \cf5 \strokec5 await\cf4 \strokec4  db.users.find_one\strokec6 (\{\cf2 \strokec2 "id"\cf4 \strokec6 :\strokec4  sub\strokec6 \},\strokec4  \strokec6 \{\cf2 \strokec2 "_id"\cf4 \strokec6 :\strokec4  \cf7 \strokec7 0\cf4 \strokec6 \})\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  user\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 401\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Utente non trovato"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  user\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  require_admin\strokec6 (\strokec4 user\strokec6 :\strokec4  \cf5 \strokec5 dict\cf4 \strokec4  = Depends\strokec6 (\strokec4 current_user\strokec6 ))\strokec4  -> \cf5 \strokec5 dict\cf4 \strokec6 :\cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf5 \strokec5 if\cf4 \strokec4  user\strokec6 [\cf2 \strokec2 "role"\cf4 \strokec6 ]\strokec4  != \cf2 \strokec2 "admin"\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\strokec6 (\cf7 \strokec7 403\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "Riservato agli amministratori"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  user\cb1 \
\
}