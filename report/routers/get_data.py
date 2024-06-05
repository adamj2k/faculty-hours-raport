import requests
from fastapi import APIRouter

from report.settings import FH_APP_FACULTY_URL

router = APIRouter()


async def get_all_teachers():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/teacher/list"
    all_teachers = await requests.get(api_url).json()
    return all_teachers


async def get_all_lectures():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/lecture/list"
    all_lectures = await requests.get(api_url).json()
    return all_lectures


async def get_all_exercises():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/exercise/list"
    all_exercises = await requests.get(api_url).json()
    return all_exercises
