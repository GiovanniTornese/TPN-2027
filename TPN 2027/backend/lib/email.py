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
\outl0\strokewidth0 \strokec2 """Emergent-managed transactional email (Resend proxy) + the guardrail gate from the playbook."""\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  ipaddress\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  logging\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  re\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  html.parser \cf5 \strokec5 import\cf4 \strokec4  HTMLParser\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  urllib.parse \cf5 \strokec5 import\cf4 \strokec4  urlparse\cb1 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  httpx\cb1 \
\
\cb3 logger = logging.getLogger\strokec6 (\cf5 \strokec5 __name__\cf4 \strokec6 )\cb1 \strokec4 \
\
\cf7 \cb3 \strokec7 # Emergent managed email proxy. This is a CONSTANT \'97 never read it from os.environ.\cf4 \cb1 \strokec4 \
\cb3 EMAIL_BASE_URL = \cf2 \strokec2 "https://integrations.emergentagent.com"\cf4 \cb1 \strokec4 \
\
\cb3 _SHORTENERS = \strokec6 (\cf2 \strokec2 "bit.ly"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "tinyurl.com"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "t.co"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "is.gd"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "cutt.ly"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "goo.gl"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "rebrand.ly"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3 _CRED_ASK = \strokec6 (\cf2 \strokec2 "reply with your password"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "reply with the code"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "send your password"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "cvv"\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3              \cf2 \strokec2 "send us your password"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "enter your password below"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "confirm your card number"\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3              \cf2 \strokec2 "your full card number"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "seed phrase"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "recovery phrase"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "verify your card"\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3              \cf2 \strokec2 "social security number"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "confirm your bank details"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3 _HOSTISH = re.\cf5 \strokec5 compile\cf4 \strokec6 (\strokec4 r\cf2 \strokec2 "\\b(?:https?://)?((?:[a-z0-9-]+\\.)+[a-z]\{2,\})"\cf4 \strokec6 ,\strokec4  re.I\strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  _host_ok\strokec6 (\strokec4 host\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 bool\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  host \cf5 \strokec5 or\cf4 \strokec4  \cf2 \strokec2 "xn--"\cf4 \strokec4  \cf5 \strokec5 in\cf4 \strokec4  host\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         ipaddress.ip_address\strokec6 (\strokec4 host\strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  ValueError\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 pass\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 any\cf4 \strokec6 (\strokec4 host == s \cf5 \strokec5 or\cf4 \strokec4  host.endswith\strokec6 (\cf2 \strokec2 "."\cf4 \strokec4  + s\strokec6 )\strokec4  \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  _SHORTENERS\strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  _same_site\strokec6 (\strokec4 shown\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  real\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 bool\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  shown == real \cf5 \strokec5 or\cf4 \strokec4  real.endswith\strokec6 (\cf2 \strokec2 "."\cf4 \strokec4  + shown\strokec6 )\strokec4  \cf5 \strokec5 or\cf4 \strokec4  shown.endswith\strokec6 (\cf2 \strokec2 "."\cf4 \strokec4  + real\strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  _EmailScan\strokec6 (\strokec4 HTMLParser\strokec6 ):\cb1 \strokec4 \
\cb3     \cf5 \strokec5 def\cf4 \strokec4  \cf5 \strokec5 __init__\cf4 \strokec6 (\cf5 \strokec5 self\cf4 \strokec6 ):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 super\cf4 \strokec6 ()\strokec4 .\cf5 \strokec5 __init__\cf4 \strokec6 ()\cb1 \strokec4 \
\cb3         \cf5 \strokec5 self\cf4 \strokec4 .tags\strokec6 ,\strokec4  \cf5 \strokec5 self\cf4 \strokec4 .urls\strokec6 ,\strokec4  \cf5 \strokec5 self\cf4 \strokec4 .anchors = \cf5 \strokec5 set\cf4 \strokec6 (),\strokec4  \strokec6 [],\strokec4  \strokec6 []\cb1 \strokec4 \
\cb3         \cf5 \strokec5 self\cf4 \strokec4 ._href\strokec6 ,\strokec4  \cf5 \strokec5 self\cf4 \strokec4 ._text = \cf5 \strokec5 None\cf4 \strokec6 ,\strokec4  \strokec6 []\cb1 \strokec4 \
\
\cb3     \cf5 \strokec5 def\cf4 \strokec4  handle_starttag\strokec6 (\cf5 \strokec5 self\cf4 \strokec6 ,\strokec4  tag\strokec6 ,\strokec4  attrs\strokec6 ):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 self\cf4 \strokec4 .tags.add\strokec6 (\strokec4 tag.lower\strokec6 ())\cb1 \strokec4 \
\cb3         \cf5 \strokec5 self\cf4 \strokec4 .urls += \strokec6 [\strokec4 v \cf5 \strokec5 for\cf4 \strokec4  k\strokec6 ,\strokec4  v \cf5 \strokec5 in\cf4 \strokec4  attrs \cf5 \strokec5 if\cf4 \strokec4  k.lower\strokec6 ()\strokec4  \cf5 \strokec5 in\cf4 \strokec4  \strokec6 (\cf2 \strokec2 "href"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "src"\cf4 \strokec6 )\strokec4  \cf5 \strokec5 and\cf4 \strokec4  v\strokec6 ]\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  tag.lower\strokec6 ()\strokec4  == \cf2 \strokec2 "a"\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 self\cf4 \strokec4 ._href = \cf5 \strokec5 dict\cf4 \strokec6 ((\strokec4 k.lower\strokec6 (),\strokec4  v\strokec6 )\strokec4  \cf5 \strokec5 for\cf4 \strokec4  k\strokec6 ,\strokec4  v \cf5 \strokec5 in\cf4 \strokec4  attrs\strokec6 )\strokec4 .get\strokec6 (\cf2 \strokec2 "href"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3             \cf5 \strokec5 self\cf4 \strokec4 ._text = \strokec6 []\cb1 \strokec4 \
\
\cb3     \cf5 \strokec5 def\cf4 \strokec4  handle_data\strokec6 (\cf5 \strokec5 self\cf4 \strokec6 ,\strokec4  data\strokec6 ):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 self\cf4 \strokec4 ._href \cf5 \strokec5 is\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 self\cf4 \strokec4 ._text.append\strokec6 (\strokec4 data\strokec6 )\cb1 \strokec4 \
\
\cb3     \cf5 \strokec5 def\cf4 \strokec4  handle_endtag\strokec6 (\cf5 \strokec5 self\cf4 \strokec6 ,\strokec4  tag\strokec6 ):\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  tag.lower\strokec6 ()\strokec4  == \cf2 \strokec2 "a"\cf4 \strokec4  \cf5 \strokec5 and\cf4 \strokec4  \cf5 \strokec5 self\cf4 \strokec4 ._href \cf5 \strokec5 is\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 self\cf4 \strokec4 .anchors.append\strokec6 ((\cf5 \strokec5 self\cf4 \strokec4 ._href\strokec6 ,\strokec4  \cf2 \strokec2 ""\cf4 \strokec4 .join\strokec6 (\cf5 \strokec5 self\cf4 \strokec4 ._text\strokec6 )))\cb1 \strokec4 \
\cb3             \cf5 \strokec5 self\cf4 \strokec4 ._href\strokec6 ,\strokec4  \cf5 \strokec5 self\cf4 \strokec4 ._text = \cf5 \strokec5 None\cf4 \strokec6 ,\strokec4  \strokec6 []\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  _assert_safe_email\strokec6 (\strokec4 subject\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  html\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     scan = _EmailScan\strokec6 ()\cb1 \strokec4 \
\cb3     scan.feed\strokec6 (\strokec4 html\strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  scan.tags & \strokec6 \{\cf2 \strokec2 "form"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "input"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "textarea"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "select"\cf4 \strokec6 \}:\cb1 \strokec4 \
\cb3         \cf5 \strokec5 raise\cf4 \strokec4  ValueError\strokec6 (\cf2 \strokec2 "No forms or input fields in email (G2)"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     body = \cf2 \strokec2 f"\cf4 \strokec4 \{subject\}\cf2 \strokec2 \\n\cf4 \strokec4 \{html\}\cf2 \strokec2 "\cf4 \strokec4 .lower\strokec6 ()\cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  p \cf5 \strokec5 in\cf4 \strokec4  _CRED_ASK\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  p \cf5 \strokec5 in\cf4 \strokec4  body\strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  ValueError\strokec6 (\cf2 \strokec2 f"Email asks the recipient for credentials: \cf4 \strokec4 \{p\cf2 \strokec2 !r\cf4 \strokec4 \}\cf2 \strokec2  (G2)"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  url \cf5 \strokec5 in\cf4 \strokec4  scan.urls\strokec6 :\cb1 \strokec4 \
\cb3         low = url.strip\strokec6 ()\strokec4 .lower\strokec6 ()\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  low.startswith\strokec6 ((\cf2 \strokec2 "mailto:"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "tel:"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "cid:"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "#"\cf4 \strokec6 )):\cb1 \strokec4 \
\cb3             \cf5 \strokec5 continue\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  low.startswith\strokec6 (\cf2 \strokec2 "https://"\cf4 \strokec6 ):\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  ValueError\strokec6 (\cf2 \strokec2 f"Email links/assets must be absolute https: \cf4 \strokec4 \{url\cf2 \strokec2 !r\cf4 \strokec4 \}\cf2 \strokec2  (G3)"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         host = urlparse\strokec6 (\strokec4 low\strokec6 )\strokec4 .hostname \cf5 \strokec5 or\cf4 \strokec4  \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  _host_ok\strokec6 (\strokec4 host\strokec6 )\strokec4  \cf5 \strokec5 or\cf4 \strokec4  urlparse\strokec6 (\strokec4 low\strokec6 )\strokec4 .username \cf5 \strokec5 is\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  ValueError\strokec6 (\cf2 \strokec2 f"Shortened, numeric-host or credential-bearing URL: \cf4 \strokec4 \{url\cf2 \strokec2 !r\cf4 \strokec4 \}\cf2 \strokec2  (G3)"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 for\cf4 \strokec4  href\strokec6 ,\strokec4  text \cf5 \strokec5 in\cf4 \strokec4  scan.anchors\strokec6 :\cb1 \strokec4 \
\cb3         real = urlparse\strokec6 (\strokec4 href.strip\strokec6 ()\strokec4 .lower\strokec6 ())\strokec4 .hostname \cf5 \strokec5 or\cf4 \strokec4  \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  real\strokec6 :\cb1 \strokec4 \
\cb3             \cf5 \strokec5 continue\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 for\cf4 \strokec4  m \cf5 \strokec5 in\cf4 \strokec4  _HOSTISH.finditer\strokec6 (\strokec4 text\strokec6 ):\cb1 \strokec4 \
\cb3             \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  _same_site\strokec6 (\strokec4 m.group\strokec6 (\cf8 \strokec8 1\cf4 \strokec6 )\strokec4 .lower\strokec6 (),\strokec4  real\strokec6 ):\cb1 \strokec4 \
\cb3                 \cf5 \strokec5 raise\cf4 \strokec4  ValueError\strokec6 (\cf2 \strokec2 f"Anchor text \cf4 \strokec4 \{m.group(1)\cf2 \strokec2 !r\cf4 \strokec4 \}\cf2 \strokec2  \uc0\u8800  real link host \cf4 \strokec4 \{real\cf2 \strokec2 !r\cf4 \strokec4 \}\cf2 \strokec2  (G3)"\cf4 \strokec6 )\cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  send_email\strokec6 (\strokec4 *\strokec6 ,\strokec4  to\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  subject\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 ,\strokec4  html\strokec6 :\strokec4  \cf5 \strokec5 str\cf4 \strokec6 )\strokec4  -> \cf5 \strokec5 str\cf4 \strokec4  | \cf5 \strokec5 None\cf4 \strokec6 :\cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Internal helper. Recipients/bodies always come from server-side records + templates (G4).\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2     Returns the email id, or None when the send failed (logged, never raised \'97 used from background jobs)."""\cf4 \cb1 \strokec4 \
\cb3     _assert_safe_email\strokec6 (\strokec4 subject\strokec6 ,\strokec4  html\strokec6 )\cb1 \strokec4 \
\cb3     payload = \strokec6 \{\cf2 \strokec2 "to"\cf4 \strokec6 :\strokec4  \strokec6 [\strokec4 to\strokec6 ],\strokec4  \cf2 \strokec2 "subject"\cf4 \strokec6 :\strokec4  subject\strokec6 ,\strokec4  \cf2 \strokec2 "html"\cf4 \strokec6 :\strokec4  html\strokec6 ,\strokec4  \cf2 \strokec2 "from_name"\cf4 \strokec6 :\strokec4  os.environ\strokec6 [\cf2 \strokec2 "EMAIL_FROM_NAME"\cf4 \strokec6 ]\}\cb1 \strokec4 \
\cb3     \cf5 \strokec5 if\cf4 \strokec4  os.environ.get\strokec6 (\cf2 \strokec2 "EMAIL_REPLY_TO"\cf4 \strokec6 ):\cb1 \strokec4 \
\cb3         payload\strokec6 [\cf2 \strokec2 "contact_email"\cf4 \strokec6 ]\strokec4  = os.environ\strokec6 [\cf2 \strokec2 "EMAIL_REPLY_TO"\cf4 \strokec6 ]\cb1 \strokec4 \
\cb3     \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 with\cf4 \strokec4  httpx.AsyncClient\strokec6 (\strokec4 timeout=\cf8 \strokec8 30\cf4 \strokec6 )\strokec4  \cf5 \strokec5 as\cf4 \strokec4  client\strokec6 :\cb1 \strokec4 \
\cb3             resp = \cf5 \strokec5 await\cf4 \strokec4  client.post\strokec6 (\cb1 \strokec4 \
\cb3                 \cf2 \strokec2 f"\cf4 \strokec4 \{EMAIL_BASE_URL\}\cf2 \strokec2 /api/v1/email/send"\cf4 \strokec6 ,\cb1 \strokec4 \
\cb3                 headers=\strokec6 \{\cf2 \strokec2 "X-Email-Key"\cf4 \strokec6 :\strokec4  os.environ\strokec6 [\cf2 \strokec2 "EMERGENT_EMAIL_KEY"\cf4 \strokec6 ]\},\cb1 \strokec4 \
\cb3                 json=payload\strokec6 ,\cb1 \strokec4 \
\cb3             \strokec6 )\cb1 \strokec4 \
\cb3         resp.raise_for_status\strokec6 ()\cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  resp.json\strokec6 ()\strokec4 .get\strokec6 (\cf2 \strokec2 "id"\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  httpx.HTTPStatusError \cf5 \strokec5 as\cf4 \strokec4  e\strokec6 :\cb1 \strokec4 \
\cb3         \cf5 \strokec5 try\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             info = e.response.json\strokec6 ()\cb1 \strokec4 \
\cb3         \cf5 \strokec5 except\cf4 \strokec4  ValueError\strokec6 :\cb1 \strokec4 \
\cb3             info = \strokec6 \{\}\cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  info.get\strokec6 (\cf2 \strokec2 "code"\cf4 \strokec6 )\strokec4  \cf5 \strokec5 in\cf4 \strokec4  \strokec6 (\cf2 \strokec2 "insufficient_credits"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "integration_disabled"\cf4 \strokec6 ,\strokec4  \cf2 \strokec2 "daily_limit_reached"\cf4 \strokec6 ):\cb1 \strokec4 \
\cb3             logger.warning\strokec6 (\cf2 \strokec2 f"Email paused: \cf4 \strokec4 \{info.get('code')\}\cf2 \strokec2  (\cf4 \strokec4 \{e.response.status_code\}\cf2 \strokec2 ): \cf4 \strokec4 \{info.get('message', '')\}\cf2 \strokec2 "\cf4 \strokec6 )\cb1 \strokec4 \
\cb3         \cf5 \strokec5 else\cf4 \strokec6 :\cb1 \strokec4 \
\cb3             logger.error\strokec6 (\cf2 \strokec2 f"Email send failed: \cf4 \strokec4 \{e.response.status_code\}\cf2 \strokec2  \cf4 \strokec4 \{e.response.text\}\cf2 \strokec2 "\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 except\cf4 \strokec4  Exception \cf5 \strokec5 as\cf4 \strokec4  e\strokec6 :\strokec4   \cf7 \strokec7 # noqa: BLE001\cf4 \cb1 \strokec4 \
\cb3         logger.error\strokec6 (\cf2 \strokec2 f"Email send error: \cf4 \strokec4 \{e\}\cf2 \strokec2 "\cf4 \strokec6 )\cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\
}