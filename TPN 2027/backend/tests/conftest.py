{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red80\green173\blue77;\red16\green16\blue16;\red187\green187\blue187;
\red157\green88\blue173;\red212\green212\blue212;\red70\green137\blue204;\red191\green91\blue43;\red71\green71\blue71;
}
{\*\expandedcolortbl;;\cssrgb\c37255\c72157\c37255;\cssrgb\c7843\c7843\c7843;\cssrgb\c78039\c78039\c78039;
\cssrgb\c68235\c44314\c73333;\cssrgb\c86275\c86275\c86275;\cssrgb\c33725\c61176\c83922;\cssrgb\c80000\c43922\c21961;\cssrgb\c34902\c34902\c34902;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 """Pre-scaffolded pytest fixtures for the FastAPI backend.\cf4 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 Tests hit the live uvicorn process managed by supervisor (not an in-process ASGI app), so\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 the app under test is the same one the frontend and Playwright see. Do NOT re-create this\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 file \'97 add app-specific fixtures below the marker at the bottom.\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 """\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  os\cb1 \
\
\cf5 \cb3 \strokec5 import\cf4 \strokec4  httpx\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  pytest\cb1 \
\cf5 \cb3 \strokec5 import\cf4 \strokec4  pytest_asyncio\cb1 \
\
\cb3 BACKEND_URL = os.environ.get\cf6 \strokec6 (\cf2 \strokec2 "BACKEND_URL"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "http://localhost:8001"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3 API_URL = \cf2 \strokec2 f"\cf4 \strokec4 \{BACKEND_URL\}\cf2 \strokec2 /api"\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 def\cf4 \strokec4  api_url\cf6 \strokec6 (\cf4 \strokec4 path\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 ""\cf6 \strokec6 )\cf4 \strokec4  -> \cf5 \strokec5 str\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Absolute URL for an /api route: api_url("/status") -> http://localhost:8001/api/status."""\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  \cf2 \strokec2 f"\cf4 \strokec4 \{API_URL\}\{path\}\cf2 \strokec2 "\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 @pytest\cf4 \strokec4 .fixture\cf6 \strokec6 (\cf4 \strokec4 scope=\cf2 \strokec2 "session"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 def\cf4 \strokec4  backend_url\cf6 \strokec6 ()\cf4 \strokec4  -> \cf5 \strokec5 str\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 return\cf4 \strokec4  BACKEND_URL\cb1 \
\
\
\cf7 \cb3 \strokec7 @pytest\cf4 \strokec4 .fixture\cb1 \
\cf5 \cb3 \strokec5 def\cf4 \strokec4  client\cf6 \strokec6 ():\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Sync httpx client rooted at /api \'97 the default for endpoint tests.\cf4 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2     Example:\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2         def test_status(client):\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2             assert client.get("/status").status_code == 200\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2     """\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 with\cf4 \strokec4  httpx.Client\cf6 \strokec6 (\cf4 \strokec4 base_url=API_URL\cf6 \strokec6 ,\cf4 \strokec4  timeout=\cf8 \strokec8 30.0\cf6 \strokec6 )\cf4 \strokec4  \cf5 \strokec5 as\cf4 \strokec4  c\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 yield\cf4 \strokec4  c\cb1 \
\
\
\cf7 \cb3 \strokec7 @pytest_asyncio\cf4 \strokec4 .fixture\cb1 \
\cf5 \cb3 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 def\cf4 \strokec4  aclient\cf6 \strokec6 ():\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 """Async variant, for tests that also await motor/backend helpers directly."""\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 async\cf4 \strokec4  \cf5 \strokec5 with\cf4 \strokec4  httpx.AsyncClient\cf6 \strokec6 (\cf4 \strokec4 base_url=API_URL\cf6 \strokec6 ,\cf4 \strokec4  timeout=\cf8 \strokec8 30.0\cf6 \strokec6 )\cf4 \strokec4  \cf5 \strokec5 as\cf4 \strokec4  c\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 yield\cf4 \strokec4  c\cb1 \
\
\
\cf9 \cb3 \strokec9 # --- app-specific fixtures below this line ---\cf4 \cb1 \strokec4 \
\
}