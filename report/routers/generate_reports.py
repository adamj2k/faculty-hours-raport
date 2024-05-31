import json
from io import StringIO

import pandas as pd

# from get_data import get_all_teachers, get_all_lectures
from test_data import (
    all_exercises_test_data,
    all_lectures_test_data,
    all_teachers_test_data,
)


def generate_teachers_reports():
    # all_teachers = await get_all_teachers()
    # all_lectures = await get_all_lectures()
    all_exercises = []  # TODO: add get all exercises
    all_exercises_test_data_json = StringIO(
        json.dumps(all_exercises_test_data["exercises"], indent=4)
    )
    all_teachers_test_data_json = StringIO(
        json.dumps(all_teachers_test_data["teachers"], indent=4)
    )
    all_lectures_test_data_json = StringIO(
        json.dumps(all_lectures_test_data["lectures"], indent=4)
    )
    df_teachers = pd.read_json(all_teachers_test_data_json, orient="records")
    print(df_teachers)
    df_lectures = pd.read_json(all_lectures_test_data_json, orient="records")
    print(df_lectures)
    df_exercises = pd.read_json(all_exercises_test_data_json, orient="records")
    print(df_exercises)
    df_report = pd.merge(df_teachers, df_lectures, left_on="id", right_on="teacher_id")
    print(df_report)
    df_complete_report = pd.merge(
        df_report, df_exercises, how="left", left_on="id_x", right_on="teacher_id"
    )
    print(df_complete_report)

    return None


generate_teachers_reports()
