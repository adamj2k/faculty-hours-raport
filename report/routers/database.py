import motor.motor_asyncio

from report.settings import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client["faculty-reports"]
teachers_reports_collection = database["teachers_reports"]
personal_workload_reports_collection = database["personal_reports"]
summary_reports_collection = database["summary_reports"]
