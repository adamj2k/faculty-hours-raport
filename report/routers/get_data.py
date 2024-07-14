import requests
from fastapi import APIRouter

from report.settings import FH_APP_FACULTY_URL

router = APIRouter()


def get_all_teachers():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/teacher/list/"
    all_teachers = requests.get(api_url).json()
    return all_teachers["teachers"]


def get_all_lectures():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/lecture/list/"
    all_lectures = requests.get(api_url).json()
    return all_lectures["lectures"]


def get_all_exercises():
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/exercise/list/"
    all_exercises = requests.get(api_url).json()
    return all_exercises["exercises"]


def get_teacher(id):
    api_url = f"http://{FH_APP_FACULTY_URL}/faculty/teacher/{id}"
    teacher = requests.get(api_url).json()
    return teacher
