import io
import json
import re

import pandas as pd


def find_teacher_id_in_body(body) -> int:
    """
    Find and extract the teacher ID from the given body.
    """
    pattern = r"id=(\d+)"
    teacher_id_list = re.findall(pattern, str(body))
    teacher_id = int(teacher_id_list[0])
    return teacher_id


def convert_data_to_int(value):
    """
    Handling missing data and convert existing numbers to int.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def convert_data_to_str(value):
    """
    Handling missing data and convert existing data to string.
    """
    try:
        return str(value)
    except (ValueError, TypeError):
        return ""


def convert_data_to_data_frame(data):
    """
    Convert data from faculty service to pandas data frame.
    """
    return pd.read_json(io.StringIO(json.dumps(data)), orient="records")


def make_empty_personal_workload_report(teacher_id: int, teacher: dict) -> pd.DataFrame:
    """
    Make empty personal workload report as data frame, when
    teacher doesn't have any lecture or exercise.
    Parameters:
        teacher_id (int): The ID of the teacher.
        teacher (dict): Dictionary with teacher information.
    Returns:
        pd.DataFrame: DataFrame containing the empty personal workload report.
    """
    return pd.DataFrame(
        {
            "id": [teacher_id],
            "teacher": [teacher["name"] + " " + teacher["last_name"]],
            "hours_semester1": [0],
            "hours_semester2": [0],
            "pensum": [0],
            "sum_hours": [0],
            "difference_pensum_sum_hours": [0],
        }
    )


def make_personal_workload_report_with_data(
    teacher_id: int,
    teacher: dict,
    df_lectures_teacher: pd.DataFrame,
    df_exercises_teacher: pd.DataFrame,
) -> pd.DataFrame:
    """
    Make personal workload report with provided data for a teacher.
    Parameters:
        teacher_id (int): The ID of the teacher.
        teacher (dict): Dictionary with teacher information.
        df_lectures_teacher (pd.DataFrame): Pandas DataFrame of lectures for the teacher.
        df_exercises_teacher (pd.DataFrame): Pandas DataFrame of exercises for the teacher.
    Returns:
        pd.DataFrame: DataFrame containing the complete personal workload report.
    """
    df_join_lectures_exercises = pd.concat([df_lectures_teacher, df_exercises_teacher])
    df_semesters = df_join_lectures_exercises.groupby("semester", as_index=False).sum()
    df_complete_report = pd.DataFrame(
        {
            "id": [teacher_id],
            "teacher": [teacher["name"] + " " + teacher["last_name"]],
            "hours_semester1": [
                df_semesters["sum_lectures_hours"][0]
                + df_semesters["sum_exercises_hours"][0]
            ],
            "hours_semester2": [
                df_semesters["sum_lectures_hours"][1]
                + df_semesters["sum_exercises_hours"][1]
            ],
            "pensum": [240],
        }
    )
    df_complete_report["sum_hours"] = (
        df_complete_report["hours_semester1"] + df_complete_report["hours_semester2"]
    )
    df_complete_report["difference_pensum_sum_hours"] = (
        df_complete_report["pensum"] - df_complete_report["sum_hours"]
    )
    return df_complete_report


def prepare_teachers_for_summary_report(
    df_teachers: pd.DataFrame, df_lectures: pd.DataFrame, df_exercises: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepare a DataFrame containing the summary report for teachers based on the given DataFrames of teachers, lectures, and exercises.

    Args:
        df_teachers (pd.DataFrame): DataFrame containing information about teachers.
        df_lectures (pd.DataFrame): DataFrame containing information about lectures.
        df_exercises (pd.DataFrame): DataFrame containing information about exercises.

    Returns:
        pd.DataFrame: DataFrame containing the summary report for teachers. The DataFrame has the following columns:
            - teacher_id (int): The ID of the teacher.
            - subject (str): The subject taught by the teacher.
            - teacher_name (str): The name of the teacher.
            - lecture_teacher (int or bool): The number of lecture hours taught by the teacher. If the value is a float greater than 0, it is converted to True, otherwise False.
            - exercise_teachers (int or bool): The number of exercise hours taught by the teacher. If the value is a float greater than 0, it is converted to True, otherwise False.
            - groups_for_teacher (int): The number of groups taught by the teacher.
            - hours_for_teacher (int): The total number of hours taught by the teacher (lecture_teacher + exercise_teachers).
    """
    df_join_exercises_lectures = pd.concat([df_lectures, df_exercises])
    df_data_to_report = pd.merge(
        df_teachers,
        df_join_exercises_lectures,
        how="left",
        left_on="id",
        right_on="teacher_id",
    )
    df_data_to_report = df_data_to_report.groupby(
        ["name_x", "id_y"], as_index=False
    ).sum()
    df_teachers_for_report = pd.DataFrame(
        {
            "teacher_id": df_data_to_report["teacher_id"],
            "subject": df_data_to_report["name_y"],
            "teacher_name": df_data_to_report["name_x"]
            + " "
            + df_data_to_report["last_name"],
            "lecture_teacher": df_data_to_report["hours_lectures"],
            "exercise_teachers": df_data_to_report["hours_exercises"],
            "groups_for_teacher": df_data_to_report["groups_exercises"],
        }
    )
    df_teachers_for_report["hours_for_teacher"] = (
        df_teachers_for_report["lecture_teacher"]
        + df_teachers_for_report["exercise_teachers"]
    )
    df_data_to_report["hours_for_teacher"] = df_teachers_for_report[
        "hours_for_teacher"
    ].apply(convert_data_to_int)
    df_teachers_for_report["teacher_id"] = df_teachers_for_report["teacher_id"].apply(
        convert_data_to_int
    )
    df_teachers_for_report["groups_for_teacher"] = df_teachers_for_report[
        "groups_for_teacher"
    ].apply(convert_data_to_int)
    df_teachers_for_report["lecture_teacher"] = df_teachers_for_report[
        "lecture_teacher"
    ].apply(lambda x: x > 0 if isinstance(x, float) else False)
    df_teachers_for_report["exercise_teachers"] = df_teachers_for_report[
        "exercise_teachers"
    ].apply(lambda x: x > 0 if isinstance(x, float) else False)

    return df_teachers_for_report


def get_teacher_list_to_data_frame(
    teachers_ids: list, subject: str, teachers: pd.DataFrame
) -> list:
    """
    Generate a list of teacher information as dictionaries based on a list of teacher IDs and a subject.

    Args:
        teachers_ids (list): A list of teacher IDs.
        subject (str): The subject to filter the teachers by.
        teachers (pd.DataFrame): The DataFrame containing the teacher information.

    Returns:
        list: A list of dictionaries, where each dictionary represents the teacher information for a single teacher.
              Each dictionary contains the following keys:
              - 'teacher_name' (str): The name of the teacher.
              - 'lecture_teacher' (bool): True if teacher conducts lecture hours, False otherwise.
              - 'exercise_teachers' (bool): true if teacher conducts exercise hours, False otherwise.
              - 'groups_for_teacher' (int): The number of groups taught by the teacher.
              - 'hours_for_teacher' (int): The total number of hours taught by the teacher.
    """
    teachers_list = []
    for teacher_id in teachers_ids:
        teacher_info = teachers[
            (teachers["teacher_id"] == teacher_id) & (teachers["subject"] == subject)
        ]
        teacher_info = teacher_info[
            [
                "teacher_name",
                "lecture_teacher",
                "exercise_teachers",
                "groups_for_teacher",
                "hours_for_teacher",
            ]
        ]
        if not teacher_info.empty:
            teachers_list.extend(teacher_info.to_dict(orient="records"))
    return teachers_list


def make_summary_classes_department_report(
    df_lectures: pd.DataFrame, df_exercises: pd.DataFrame, df_teachers: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate a summary report of classes and departments based on the provided data frames.

    Args:
        df_lectures (pd.DataFrame): Data frame containing lectures data.
        df_exercises (pd.DataFrame): Data frame containing exercises data.
        df_teachers (pd.DataFrame): Data frame containing teachers data.

    Returns:
        pd.DataFrame: Summary report of classes and departments.
    """
    df_concat_exercises_lectures = pd.concat([df_lectures, df_exercises])
    columns_to_sum = ["hours_lectures", "hours_exercises", "groups_exercises"]
    other_columns = [
        column
        for column in df_concat_exercises_lectures.columns
        if column not in columns_to_sum
    ]
    df_list_teachers = (
        df_concat_exercises_lectures.groupby("name")["teacher_id"]
        .apply(list)
        .reset_index()
    )
    df_from_other_columns = (
        df_concat_exercises_lectures[other_columns]
        .groupby("name")
        .first()
        .reset_index()
    )
    df_group_by = (
        df_concat_exercises_lectures.groupby("name")[columns_to_sum].sum().reset_index()
    )
    result1 = pd.merge(df_group_by, df_from_other_columns, on="name")
    result = pd.merge(result1, df_list_teachers, on="name")
    teachers = prepare_teachers_for_summary_report(
        df_teachers, df_lectures, df_exercises
    )
    summary_report = pd.DataFrame(
        {
            "subject": result["name"],
            "faculty": "faculty of study",
            "study_year": result["study_year"],
            "semester": result["semester"],
            "hours_lectures": result["sum_lectures_hours"],
            "hours_exercises": result["sum_exercises_hours"],
            "groups": result["groups_exercises"],
            "teachers": result["teacher_id_y"],
        }
    )
    summary_report["subject"] = summary_report["subject"].apply(convert_data_to_str)
    summary_report["study_year"] = summary_report["study_year"].apply(
        convert_data_to_int
    )
    summary_report["semester"] = summary_report["semester"].apply(convert_data_to_int)
    summary_report["hours_lectures"] = summary_report["hours_lectures"].apply(
        convert_data_to_int
    )
    summary_report["hours_exercises"] = summary_report["hours_exercises"].apply(
        convert_data_to_int
    )
    summary_report["groups"] = summary_report["groups"].apply(convert_data_to_int)
    summary_report["teachers"] = summary_report.apply(
        lambda row: get_teacher_list_to_data_frame(
            row["teachers"], row["subject"], teachers
        ),
        axis=1,
    )
    return summary_report
