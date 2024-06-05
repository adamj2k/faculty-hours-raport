import pandas as pd

from report.routers.get_data import (
    get_all_exercises,
    get_all_lectures,
    get_all_teachers,
)


def generate_teachers_reports():
    all_teachers = get_all_teachers()
    all_lectures = get_all_lectures()
    all_exercises = get_all_exercises()
    df_teachers = pd.read_json(all_teachers, orient="records")
    df_lectures = pd.read_json(all_lectures, orient="records")
    df_exercises = pd.read_json(all_exercises, orient="records")
    df_join_teachers_lectures = pd.merge(
        df_teachers, df_lectures, left_on="id", right_on="teacher_id"
    )
    df_data_to_report = pd.merge(
        df_join_teachers_lectures,
        df_exercises,
        how="left",
        left_on="id_x",
        right_on="teacher_id",
    )
    df_complete_report = df_data_to_report.groupby(["id_x"]).sum()

    return df_complete_report
