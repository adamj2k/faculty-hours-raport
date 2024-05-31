import requests
import settings
from fastapi import APIRouter

router = APIRouter()


async def get_all_teachers():
    api_url = f"http://faculty-hours-faculty-web-1:8100/faculty/teachers"  # TODO: change url in env files
    all_teachers = requests.get(api_url).json()
    return all_teachers


async def get_all_lectures():
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/lectures"
    all_lectures = await requests.get(api_url).json()
    return all_lectures
