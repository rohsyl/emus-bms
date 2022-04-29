import os
from dotenv import load_dotenv
load_dotenv()

# config
ID = os.getenv("ID")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DB_LOCAL_PASS = os.getenv("DB_LOCAL_PASS")
DB_LOCAL_HOST = os.getenv("DB_LOCAL_HOST")
DB_LOCAL_NAME = os.getenv("DB_LOCAL_NAME")
DB_LOCAL_USER = os.getenv("DB_LOCAL_USER")

DB_SYNC_HOST = os.getenv("DB_SYNC_HOST")
DB_SYNC_NAME = os.getenv("DB_SYNC_NAME")
DB_SYNC_USER = os.getenv("DB_SYNC_USER")
DB_SYNC_PASS = os.getenv("DB_SYNC_PASS")
