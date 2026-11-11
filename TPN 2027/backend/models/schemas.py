"""Pydantic models \'97 every one mirrored by a TS interface in frontend/src/lib/types.ts."""\cf4 \cb1 \strokec4 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  datetime \cf5 \strokec5 import\cf4 \strokec4  datetime\cb1 \
\cf5 \cb3 \strokec5 from\cf4 \strokec4  typing \cf5 \strokec5 import\cf4 \strokec4  Literal\cf6 \strokec6 ,\cf4 \strokec4  Optional\cb1 \
\
\cf5 \cb3 \strokec5 from\cf4 \strokec4  pydantic \cf5 \strokec5 import\cf4 \strokec4  BaseModel\cf6 \strokec6 ,\cf4 \strokec4  EmailStr\cf6 \strokec6 ,\cf4 \strokec4  Field\cf6 \strokec6 ,\cf4 \strokec4  field_validator\cf6 \strokec6 ,\cf4 \strokec4  model_validator\cb1 \
\
\cb3 Gender = Literal\cf6 \strokec6 [\cf2 \strokec2 "M"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "F"\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3 Role = Literal\cf6 \strokec6 [\cf2 \strokec2 "admin"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "volunteer"\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3 ShiftRole = Literal\cf6 \strokec6 [\cf2 \strokec2 "leader"\cf6 \strokec6 ,\cf4 \strokec4  \cf2 \strokec2 "member"\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\cb3 DATE_PATTERN = r\cf2 \strokec2 "^\\d\{4\}-\\d\{2\}-\\d\{2\}$"\cf4 \cb1 \strokec4 \
\cb3 HM_PATTERN = r\cf2 \strokec2 "^([01]\\d|2[0-3]):[0-5]\\d$"\cf4 \cb1 \strokec4 \
\cb3 SLOT_PATTERN = r\cf2 \strokec2 "^([01]\\d|2[0-1]):[0-5]\\d$"\cf4 \strokec4   \cf7 \strokec7 # quick-pick 2h presets: last start 21:59\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 # ---------- users ----------\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 class\cf4 \strokec4  UserPublic\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     email\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     role\cf6 \strokec6 :\cf4 \strokec4  Role\cb1 \
\cb3     first_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3     last_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3     phone\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3     gender\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf4 \strokec4 Gender\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3     is_team_leader\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     has_password\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ProfileIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     first_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 60\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     last_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 60\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     phone\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 5\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 30\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     gender\cf6 \strokec6 :\cf4 \strokec4  Gender\cb1 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  RegisterIn\cf6 \strokec6 (\cf4 \strokec4 ProfileIn\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     email\cf6 \strokec6 :\cf4 \strokec4  EmailStr\cb1 \
\cb3     password\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 6\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 128\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  VolunteerAdminIn\cf6 \strokec6 (\cf4 \strokec4 ProfileIn\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     is_team_leader\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     email\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf4 \strokec4 EmailStr\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3     new_password\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 default=\cf5 \strokec5 None\cf6 \strokec6 ,\cf4 \strokec4  min_length=\cf8 \strokec8 6\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 128\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  VolunteerCreateIn\cf6 \strokec6 (\cf4 \strokec4 RegisterIn\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     is_team_leader\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  LoginIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     email\cf6 \strokec6 :\cf4 \strokec4  EmailStr\cb1 \
\cb3     password\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  GoogleSessionIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     session_id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  CredentialsIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     email\cf6 \strokec6 :\cf4 \strokec4  EmailStr\cb1 \
\cb3     current_password\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 ""\cf4 \cb1 \strokec4 \
\cb3     new_password\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 default=\cf5 \strokec5 None\cf6 \strokec6 ,\cf4 \strokec4  min_length=\cf8 \strokec8 6\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 128\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  VolunteerOut\cf6 \strokec6 (\cf4 \strokec4 UserPublic\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     shift_count\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \strokec4  = \cf8 \strokec8 0\cf4 \cb1 \strokec4 \
\cb3     upcoming_count\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \strokec4  = \cf8 \strokec8 0\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 # ---------- config ----------\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 class\cf4 \strokec4  Station\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     key\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     color\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = \cf2 \strokec2 "emerald"\cf4 \cb1 \strokec4 \
\cb3     archived\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  StationIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 40\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  SlotsOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     slots\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  SlotsIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     slots\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 16\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\cb3     \cf9 \strokec9 @field_validator\cf6 \strokec6 (\cf2 \strokec2 "slots"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf9 \strokec9 @classmethod\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 def\cf4 \strokec4  check_slots\cf6 \strokec6 (\cf4 \strokec4 cls\cf6 \strokec6 ,\cf4 \strokec4  v\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ])\cf4 \strokec4  -> \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]:\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 import\cf4 \strokec4  re\cb1 \
\
\cb3         \cf5 \strokec5 for\cf4 \strokec4  s \cf5 \strokec5 in\cf4 \strokec4  v\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 not\cf4 \strokec4  re.\cf5 \strokec5 match\cf6 \strokec6 (\cf4 \strokec4 SLOT_PATTERN\cf6 \strokec6 ,\cf4 \strokec4  s\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3                 \cf5 \strokec5 raise\cf4 \strokec4  ValueError\cf6 \strokec6 (\cf2 \strokec2 f"Orario non valido: \cf4 \strokec4 \{s\}\cf2 \strokec2  (formato HH:MM, max 21:00)"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 sorted\cf6 \strokec6 (\cf5 \strokec5 set\cf6 \strokec6 (\cf4 \strokec4 v\cf6 \strokec6 ))\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  TodayOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     today\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 # ---------- shifts ----------\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ShiftIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     station\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     date\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 pattern=DATE_PATTERN\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     start\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 pattern=HM_PATTERN\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     end\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 pattern=HM_PATTERN\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\cb3     \cf9 \strokec9 @model_validator\cf6 \strokec6 (\cf4 \strokec4 mode=\cf2 \strokec2 "after"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 def\cf4 \strokec4  check_range\cf6 \strokec6 (\cf5 \strokec5 self\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 self\cf4 \strokec4 .end <= \cf5 \strokec5 self\cf4 \strokec4 .start\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  ValueError\cf6 \strokec6 (\cf2 \strokec2 "L'orario di fine deve essere successivo all'inizio"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  \cf5 \strokec5 self\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ShiftCreateIn\cf6 \strokec6 (\cf4 \strokec4 ShiftIn\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     repeat_until\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 default=\cf5 \strokec5 None\cf6 \strokec6 ,\cf4 \strokec4  pattern=DATE_PATTERN\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  JoinIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     as_role\cf6 \strokec6 :\cf4 \strokec4  ShiftRole = \cf2 \strokec2 "member"\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  AssignIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     user_id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     as_role\cf6 \strokec6 :\cf4 \strokec4  ShiftRole = \cf2 \strokec2 "member"\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ShiftVolunteer\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     first_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     last_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     gender\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf4 \strokec4 Gender\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3     phone\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \strokec4   \cf7 \strokec7 # admin only\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ShiftOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     station\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     date\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     start\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     end\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     leader\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf4 \strokec4 ShiftVolunteer\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3     members\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ShiftVolunteer\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3     missing_leader\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \cb1 \strokec4 \
\cb3     free_member_slots\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     free_slots\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     is_complete\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \cb1 \strokec4 \
\cb3     is_mine\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \cb1 \strokec4 \
\cb3     my_role\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf4 \strokec4 ShiftRole\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \cb1 \strokec4 \
\cb3     has_ended\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\cb3     my_report_done\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ShiftBulkOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     created\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ShiftOut\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3     skipped_dates\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  MonthUsageOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     month\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     used\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     limit\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 # ---------- reports (resoconto fine turno) ----------\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ReportIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     hours\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 ge=\cf8 \strokec8 0.5\cf6 \strokec6 ,\cf4 \strokec4  le=\cf8 \strokec8 2\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     publications\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 ge=\cf8 \strokec8 0\cf6 \strokec6 ,\cf4 \strokec4  le=\cf8 \strokec8 10000\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     comment\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 default=\cf2 \strokec2 ""\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 2000\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\
\cb3     \cf9 \strokec9 @field_validator\cf6 \strokec6 (\cf2 \strokec2 "hours"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     \cf9 \strokec9 @classmethod\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 def\cf4 \strokec4  half_steps\cf6 \strokec6 (\cf4 \strokec4 cls\cf6 \strokec6 ,\cf4 \strokec4  v\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf6 \strokec6 )\cf4 \strokec4  -> \cf5 \strokec5 float\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 if\cf4 \strokec4  \cf5 \strokec5 round\cf6 \strokec6 (\cf4 \strokec4 v * \cf8 \strokec8 2\cf6 \strokec6 )\cf4 \strokec4  != v * \cf8 \strokec8 2\cf6 \strokec6 :\cf4 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 raise\cf4 \strokec4  ValueError\cf6 \strokec6 (\cf2 \strokec2 "Le ore vanno indicate a mezz'ore (0,5 \'96 1 \'96 1,5 \'96 2)"\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 return\cf4 \strokec4  v\cb1 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  ReportOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     shift_id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     user_id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     user_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     station\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     date\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     start\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     end\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     hours\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf4 \cb1 \strokec4 \
\cb3     publications\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     comment\cf6 \strokec6 :\cf4 \strokec4  Optional\cf6 \strokec6 [\cf5 \strokec5 str\cf6 \strokec6 ]\cf4 \strokec4  = \cf5 \strokec5 None\cf4 \strokec4   \cf7 \strokec7 # admin + author only\cf4 \cb1 \strokec4 \
\cb3     updated_at\cf6 \strokec6 :\cf4 \strokec4  datetime\cb1 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  MyReportsOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     total_hours\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf4 \cb1 \strokec4 \
\cb3     total_publications\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     reports\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ReportOut\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3     pending\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ShiftOut\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  VolunteerTotals\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     user_id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     user_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     hours\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf4 \cb1 \strokec4 \
\cb3     publications\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     reports\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  AdminReportsOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     total_hours\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 float\cf4 \cb1 \strokec4 \
\cb3     total_publications\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     total_reports\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 int\cf4 \cb1 \strokec4 \
\cb3     by_volunteer\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 VolunteerTotals\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\cb3     reports\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ReportOut\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  RemindersOut\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     tomorrow\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     shifts\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 list\cf6 \strokec6 [\cf4 \strokec4 ShiftOut\cf6 \strokec6 ]\cf4 \cb1 \strokec4 \
\
\
\cf7 \cb3 \strokec7 # ---------- announcements ----------\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 class\cf4 \strokec4  AnnouncementIn\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     title\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 120\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     body\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \strokec4  = Field\cf6 \strokec6 (\cf4 \strokec4 min_length=\cf8 \strokec8 1\cf6 \strokec6 ,\cf4 \strokec4  max_length=\cf8 \strokec8 4000\cf6 \strokec6 )\cf4 \cb1 \strokec4 \
\cb3     pinned\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \strokec4  = \cf5 \strokec5 False\cf4 \cb1 \strokec4 \
\
\
\cf5 \cb3 \strokec5 class\cf4 \strokec4  Announcement\cf6 \strokec6 (\cf4 \strokec4 BaseModel\cf6 \strokec6 ):\cf4 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 id\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     title\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     body\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     pinned\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 bool\cf4 \cb1 \strokec4 \
\cb3     author_name\cf6 \strokec6 :\cf4 \strokec4  \cf5 \strokec5 str\cf4 \cb1 \strokec4 \
\cb3     created_at\cf6 \strokec6 :\cf4 \strokec4  datetime\cb1 \
\
}
