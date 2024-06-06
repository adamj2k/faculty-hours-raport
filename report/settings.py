import os

from dotenv import load_dotenv

load_dotenv()

MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGODB_URL = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongos-report:27017/admin?authSource=admin"
FH_APP_FACULTY_URL = os.getenv("FH_APP_FACULTY_URL")
