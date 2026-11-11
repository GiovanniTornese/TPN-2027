{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red80\green173\blue77;\red16\green16\blue16;\red187\green187\blue187;
\red157\green88\blue173;\red212\green212\blue212;\red191\green91\blue43;\red71\green71\blue71;\red70\green137\blue204;
}
{\*\expandedcolortbl;;\cssrgb\c37255\c72157\c37255;\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;
\cssrgb\c68235\c44314\c73333;\cssrgb\c86275\c86275\c86275;\cssrgb\c80000\c43922\c21961;\cssrgb\c34902\c34902\c34902;\cssrgb\c33725\c61176\c83922;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 """Platform cron: day-before shift reminder emails (see .emergent/crons.yml)."""\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  asyncio\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  hmac\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  logging\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  datetime \cf5 \strokec5 import\cf4 \strokec4  date \cf5 \strokec5 as\cf4 \strokec4  Date\cf6 \strokec6 ,\cf4 \strokec4  datetime\cf6 \strokec6 ,\cf4 \strokec4  timedelta\cf6 \strokec6 ,\cf4 \strokec4  timezone\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  html \cf5 \strokec5 import\cf4 \strokec4  escape\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  fastapi \cf5 \strokec5 import\cf4 \strokec4  APIRouter\cf6 \strokec6 ,\cf4 \strokec4  HTTPException\cf6 \strokec6 ,\cf4 \strokec4  Request\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.dates \cf5 \strokec5 import\cf4 \strokec4  today_iso\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.db \cf5 \strokec5 import\cf4 \strokec4  db\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  lib.email \cf5 \strokec5 import\cf4 \strokec4  send_email\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  pymongo.errors \cf5 \strokec5 import\cf4 \strokec4  DuplicateKeyError\cb1 \
\
\cb3 router = APIRouter\cf6 \strokec6 ()\cf4 \cb1 \strokec4 \
\cb3 logger = logging.getLogger\cf6 \strokec6 (\cf5 \strokec5 __name__\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3 _tasks\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 set\cf6 \strokec6 [\cf4 \strokec4 asyncio.Task\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 set\cf6 \strokec6 ()\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  _authorized\cf6 \strokec6 (\cf4 \strokec4 request\cf6 \strokec6 :\cf4 \strokec4  Request\cf6 \strokec6 )\cf4 \strokec4  -> \cf5 \strokec5 bool\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3     secret = os.environ.get\cf6 \strokec6 (\cf2 \strokec2 "WEBHOOK_CRON_SECRET"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 ""\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     header = request.headers.get\cf6 \strokec6 (\cf2 \strokec2 "authorization"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 ""\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  secret \cf5 \strokec5 or\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  header.startswith\cf6 \strokec6 (\cf2 \strokec2 "Bearer "\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  hmac.compare_digest\cf6 \strokec6 (\cf4 \strokec4 header\cf6 \strokec6 [\cf7 \strokec7 7\cf6 \strokec6 :]\cf4 \strokec4 .encode\cf6 \strokec6 (),\cf4 \strokec4  secret.encode\cf6 \strokec6 ())\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  reminder_html\cf6 \strokec6 (\cf4 \strokec4 first_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  rows\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 tuple\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 ]],\cf4 \strokec4  day_label\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 )\cf4 \strokec4  -> \cf5 \strokec5 str\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3     brand = escape\cf6 \strokec6 (\cf4 \strokec4 os.environ.get\cf6 \strokec6 (\cf2 \strokec2 "EMAIL_FROM_NAME"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "TPN 2027"\cf6 \strokec6 ))\cf4 \cb1 \strokec4 \
\cb3     items = \cf2 \strokec2 ""\cf4 \strokec4 .join\cf6 \strokec6 (\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<tr><td style="padding:8px 0;border-bottom:1px solid #e2e8f0"><strong>\cf4 \strokec4 \{escape(t)\}\cf2 \strokec2 </strong> \'b7 \cf4 \strokec4 \{escape(st)\}\cf2 \strokec2 '\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<br><span style="color:#475569">Ruolo: \cf4 \strokec4 \{escape(role)\}\cf2 \strokec2 </span></td></tr>'\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  t\cf6 \strokec6 ,\cf4 \strokec4  st\cf6 \strokec6 ,\cf4 \strokec4  role \cf5 \strokec5 in\cf4 \strokec4  rows\cb1 \
\cb3     \cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf6 \strokec6 (\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 '<table role="presentation" width="100%" style="background:#f8fafc"><tr><td style="padding:24px;font-family:Arial,sans-serif;color:#0f172a">'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<h2 style="margin:0 0 12px">Promemoria turno di domani</h2>'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<p>Ciao \cf4 \strokec4 \{escape(first_name)\}\cf2 \strokec2 , ti ricordiamo che <strong>\cf4 \strokec4 \{escape(day_label)\}\cf2 \strokec2 </strong> sei in turno:</p>'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<table role="presentation" width="100%">\cf4 \strokec4 \{items\}\cf2 \strokec2 </table>'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 '<p>Se non puoi partecipare, cancella l\\'iscrizione dall\\'app il prima possibile cos\'ec un altro volontario pu\'f2 prendere il tuo posto.</p>'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 f'<p style="font-size:12px;color:#64748b">Inviato da \cf4 \strokec4 \{brand\}\cf2 \strokec2  \'b7 Pianificazione turni.</p>'\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 '</td></tr></table>'\cf4 \cb1 \strokec4 \
\cb3     \cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  send_tomorrow_reminders\cf6 \strokec6 ()\cf4 \strokec4  -> \cf5 \strokec5 int\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3     tomorrow = \cf6 \strokec6 (\cf4 \strokec4 Date.fromisoformat\cf6 \strokec6 (\cf4 \strokec4 today_iso\cf6 \strokec6 ())\cf4 \strokec4  + timedelta\cf6 \strokec6 (\cf4 \strokec4 days=\cf7 \strokec7 1\cf6 \strokec6 ))\cf4 \strokec4 .isoformat\cf6 \strokec6 ()\cf4 \cb1 \strokec4 \
\cb3     shifts = \cf5 \strokec5 await\cf4 \strokec4  db.shifts.find\cf6 \strokec6 (\{\cf2 \strokec2 "date"\cf6 \strokec6 :\cf4 \strokec4  tomorrow\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "volunteer_ids.0"\cf6 \strokec6 :\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "$exists"\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 True\cf6 \strokec6 \}\},\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "_id"\cf6 \strokec6 :\cf4 \strokec4  \cf7 \strokec7 0\cf6 \strokec6 \})\cf4 \strokec4 .to_list\cf6 \strokec6 (\cf7 \strokec7 2000\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     stations = \cf6 \strokec6 \{\cf4 \strokec4 s\cf6 \strokec6 [\cf2 \strokec2 "key"\cf6 \strokec6 ]:\cf4 \strokec4  s\cf6 \strokec6 [\cf2 \strokec2 "name"\cf6 \strokec6 ]\cf4 \strokec4  \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  db.stations.find\cf6 \strokec6 (\{\},\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "_id"\cf6 \strokec6 :\cf4 \strokec4  \cf7 \strokec7 0\cf6 \strokec6 \})\}\cf4 \cb1 \strokec4 \
\cb3     per_user\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 dict\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 tuple\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 ,\cf4 \strokec4  \cf5 \strokec5 str\cf6 \strokec6 ]]]\cf4 \strokec4  = \cf6 \strokec6 \{\}\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  \cf5 \strokec5 sorted\cf6 \strokec6 (\cf4 \strokec4 shifts\cf6 \strokec6 ,\cf4 \strokec4  key=\cf5 \strokec5 lambda\cf4 \strokec4  x\cf6 \strokec6 :\cf4 \strokec4  x\cf6 \strokec6 [\cf2 \strokec2 "start"\cf6 \strokec6 ]):\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  uid \cf5 \strokec5 in\cf4 \strokec4  s\cf6 \strokec6 [\cf2 \strokec2 "volunteer_ids"\cf6 \strokec6 ]:\cf4 \cb1 \strokec4 \
\cb3             role = \cf2 \strokec2 "Capoturno"\cf4 \strokec4  \cf5 \strokec5 if\cf4 \strokec4  s.get\cf6 \strokec6 (\cf2 \strokec2 "leader_id"\cf6 \strokec6 )\cf4 \strokec4  == uid \cf5 \strokec5 else\cf4 \strokec4  \cf2 \strokec2 "Volontario"\cf4 \cb1 \strokec4 \
\cb3             per_user.setdefault\cf6 \strokec6 (\cf4 \strokec4 uid\cf6 \strokec6 ,\cf4 \strokec4  \cf6 \strokec6 [])\cf4 \strokec4 .append\cf6 \strokec6 ((\cf2 \strokec2 f"\cf4 \strokec4 \{s['start']\}\cf2 \strokec2 \'96\cf4 \strokec4 \{s['end']\}\cf2 \strokec2 "\cf6 \strokec6 ,\cf4 \strokec4  stations.get\cf6 \strokec6 (\cf4 \strokec4 s\cf6 \strokec6 [\cf2 \strokec2 "station"\cf6 \strokec6 ],\cf4 \strokec4  \cf2 \strokec2 "Postazione"\cf6 \strokec6 ),\cf4 \strokec4  role\cf6 \strokec6 ))\cf4 \cb1 \strokec4 \
\cb3     day_label = datetime.fromisoformat\cf6 \strokec6 (\cf4 \strokec4 tomorrow\cf6 \strokec6 )\cf4 \strokec4 .strftime\cf6 \strokec6 (\cf2 \strokec2 "%d/%m/%Y"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     sent = \cf7 \strokec7 0\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 for\cf4 \strokec4  u \cf5 \strokec5 in\cf4 \strokec4  db.users.find\cf6 \strokec6 (\{\cf2 \strokec2 "id"\cf6 \strokec6 :\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "$in"\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 (\cf4 \strokec4 per_user\cf6 \strokec6 )\}\},\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "_id"\cf6 \strokec6 :\cf4 \strokec4  \cf7 \strokec7 0\cf6 \strokec6 \}):\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 try\cf6 \strokec6 :\cf4 \strokec4   \cf8 \strokec8 # one email per person per day, never twice\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 await\cf4 \strokec4  db.reminders_sent.insert_one\cf6 \strokec6 (\{\cf2 \strokec2 "user_id"\cf6 \strokec6 :\cf4 \strokec4  u\cf6 \strokec6 [\cf2 \strokec2 "id"\cf6 \strokec6 ],\cf4 \strokec4  \cf2 \strokec2 "date"\cf6 \strokec6 :\cf4 \strokec4  tomorrow\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "at"\cf6 \strokec6 :\cf4 \strokec4  datetime.now\cf6 \strokec6 (\cf4 \strokec4 timezone.utc\cf6 \strokec6 )\})\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 except\cf4 \strokec4  DuplicateKeyError\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 continue\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 await\cf4 \strokec4  send_email\cf6 \strokec6 (\cf4 \strokec4 to=u\cf6 \strokec6 [\cf2 \strokec2 "email"\cf6 \strokec6 ],\cf4 \strokec4  subject=\cf2 \strokec2 f"Promemoria: domani sei in turno (\cf4 \strokec4 \{day_label\}\cf2 \strokec2 )"\cf6 \strokec6 ,\cf4 \cb1 \strokec4 \
\cb3                             html=reminder_html\cf6 \strokec6 (\cf4 \strokec4 u.get\cf6 \strokec6 (\cf2 \strokec2 "first_name"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 ""\cf6 \strokec6 ),\cf4 \strokec4  per_user\cf6 \strokec6 [\cf4 \strokec4 u\cf6 \strokec6 [\cf2 \strokec2 "id"\cf6 \strokec6 ]],\cf4 \strokec4  day_label\cf6 \strokec6 )):\cf4 \cb1 \strokec4 \
\cb3             sent += \cf7 \strokec7 1\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 else\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 await\cf4 \strokec4  db.reminders_sent.delete_one\cf6 \strokec6 (\{\cf2 \strokec2 "user_id"\cf6 \strokec6 :\cf4 \strokec4  u\cf6 \strokec6 [\cf2 \strokec2 "id"\cf6 \strokec6 ],\cf4 \strokec4  \cf2 \strokec2 "date"\cf6 \strokec6 :\cf4 \strokec4  tomorrow\cf6 \strokec6 \})\cf4 \cb1 \strokec4 \
\cb3     logger.info\cf6 \strokec6 (\cf2 \strokec2 f"Reminder emails sent: \cf4 \strokec4 \{sent\}\cf2 \strokec2  for \cf4 \strokec4 \{tomorrow\}\cf2 \strokec2 "\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  sent\cb1 \
\
\
\cf9 \cb3 \strokec9 @router\cf4 \strokec4 .post\cf6 \strokec6 (\cf2 \strokec2 "/cron/reminders"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  cron_reminders\cf6 \strokec6 (\cf4 \strokec4 request\cf6 \strokec6 :\cf4 \strokec4  Request\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf8 \strokec8 # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  _authorized\cf6 \strokec6 (\cf4 \strokec4 request\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\cf6 \strokec6 (\cf7 \strokec7 401\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "Unauthorized"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 try\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         envelope = \cf5 \strokec5 await\cf4 \strokec4  request.json\cf6 \strokec6 ()\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  Exception\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  HTTPException\cf6 \strokec6 (\cf7 \strokec7 400\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "Invalid body"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     run_id = request.headers.get\cf6 \strokec6 (\cf2 \strokec2 "x-webhook-id"\cf6 \strokec6 )\cf4 \strokec4  \cf5 \strokec5 or\cf4 \strokec4  \cf6 \strokec6 (\cf4 \strokec4 envelope \cf5 \strokec5 or\cf4 \strokec4  \cf6 \strokec6 \{\})\cf4 \strokec4 .get\cf6 \strokec6 (\cf2 \strokec2 "run_id"\cf6 \strokec6 )\cf4 \strokec4  \cf5 \strokec5 or\cf4 \strokec4  \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  run_id\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 try\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 await\cf4 \strokec4  db.cron_runs.insert_one\cf6 \strokec6 (\{\cf2 \strokec2 "run_id"\cf6 \strokec6 :\cf4 \strokec4  run_id\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "at"\cf6 \strokec6 :\cf4 \strokec4  datetime.now\cf6 \strokec6 (\cf4 \strokec4 timezone.utc\cf6 \strokec6 )\})\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 except\cf4 \strokec4  DuplicateKeyError\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 return\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "status"\cf6 \strokec6 :\cf4 \strokec4  \cf2 \strokec2 "duplicate"\cf6 \strokec6 \}\cf4 \cb1 \strokec4 \
\cb3     task = asyncio.create_task\cf6 \strokec6 (\cf4 \strokec4 send_tomorrow_reminders\cf6 \strokec6 ())\cf4 \cb1 \strokec4 \
\cb3     _tasks.add\cf6 \strokec6 (\cf4 \strokec4 task\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     task.add_done_callback\cf6 \strokec6 (\cf4 \strokec4 _tasks.discard\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf6 \strokec6 \{\cf2 \strokec2 "status"\cf6 \strokec6 :\cf4 \strokec4  \cf2 \strokec2 "accepted"\cf6 \strokec6 \}\cf4 \cb1 \strokec4 \
\
}