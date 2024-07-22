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
