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
    report = df_complete_report.to_json(orient="records")
    return report


def generate_personal_workload_reports(teacher_id):
    teachers_report = generate_teachers_reports()
    personal_workload_report = teachers_report.loc[teacher_id]
    report = personal_workload_report.to_json(orient="records")
    return report


def generate_summary_reports():
    all_teachers = get_all_teachers()
    all_lectures = get_all_lectures()
    all_exercises = get_all_exercises()
    df_teachers = pd.read_json(all_teachers, orient="records")
    df_lectures = pd.read_json(all_lectures, orient="records")
    df_exercises = pd.read_json(all_exercises, orient="records")
    df_concat_exercises_lectures = pd.concat([df_lectures, df_exercises])
    df_merge_with_teachers = pd.merge(
        df_concat_exercises_lectures,
        df_teachers,
        how="left",
        left_on="teacher_id",
        right_on="id",
    ).sort_values(by="name_x")
    report = df_merge_with_teachers.to_json(orient="records")
    return report
