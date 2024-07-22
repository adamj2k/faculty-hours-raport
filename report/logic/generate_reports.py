import pandas as pd

from report.routers.get_data import (
    get_all_exercises,
    get_all_lectures,
    get_all_teachers,
    get_teacher,
)
from report.utils.utils import (
    convert_data_to_data_frame,
    convert_data_to_int,
    convert_data_to_str,
    make_empty_personal_workload_report,
    make_personal_workload_report_with_data,
)


def generate_teachers_reports():
    """
    Generates a report of teachers' workload based on the data from all_teachers, all_lectures, and all_exercises.
    Returns:
        df_report (DataFrame): A DataFrame containing the following columns:
            - id (int): The teacher's ID.
            - teacher (str): The teacher's full name.
            - subject (str): The subject's name.
            - hours_lectures (int): The total hours of lectures.
            - hours_exercises (int): The total hours of exercises.
            - study_year (int): The study year.
            - semester (int): The semester.
    Note:
        - The function uses the get_all_teachers, get_all_lectures, and get_all_exercises functions to retrieve the data.
        - The data is converted to DataFrame format using the convert_data_to_data_frame function.
        - The lectures and exercises data are merged using the pd.merge function.
        - The "teacher" column is created by concatenating the "name_x" and "last_name" columns.
        - The columns to be included in the report are specified in the columns_to_move_to_report list.
        - The DataFrame is renamed using the rename function.
        - The study_year, semester, hours_lectures, and hours_exercises columns are converted to integer format using the convert_data_to_int function.
        - The subject column is converted to string format using the convert_data_to_str function.
    """
    all_teachers = get_all_teachers()
    all_lectures = get_all_lectures()
    all_exercises = get_all_exercises()
    df_teachers = convert_data_to_data_frame(all_teachers)
    df_lectures = convert_data_to_data_frame(all_lectures)
    df_exercises = convert_data_to_data_frame(all_exercises)
    df_join_exercises_lectures = pd.concat([df_lectures, df_exercises])
    df_data_to_report = pd.merge(
        df_teachers,
        df_join_exercises_lectures,
        how="left",
        left_on="id",
        right_on="teacher_id",
    )
    df_data_to_report["teacher"] = (
        df_data_to_report["name_x"] + " " + df_data_to_report["last_name"]
    )
    columns_to_move_to_report = [
        "id_x",
        "teacher",
        "name_y",
        "hours_lectures",
        "hours_exercises",
        "study_year",
        "semester",
    ]
    df_report = df_data_to_report[columns_to_move_to_report].copy()
    df_report = df_report.rename(columns={"id_x": "id", "name_y": "subject"})
    df_report["study_year"] = df_report["study_year"].apply(convert_data_to_int)
    df_report["semester"] = df_report["semester"].apply(convert_data_to_int)
    df_report["hours_lectures"] = df_report["hours_lectures"].apply(convert_data_to_int)
    df_report["hours_exercises"] = df_report["hours_exercises"].apply(
        convert_data_to_int
    )
    df_report["subject"] = df_report["subject"].apply(convert_data_to_str)
    return df_report


def generate_personal_workload_reports(teacher_id: int):
    """
    Generate personal workload reports for a given teacher.
    If teacher has no lectures or exercises, an empty report is created.
    Args:
        teacher_id (int): The ID of the teacher.
    Returns:
        pd.DataFrame: The complete personal workload report.
    """
    teacher = get_teacher(teacher_id)
    all_lectures = get_all_lectures()
    all_exercises = get_all_exercises()
    df_lectures = convert_data_to_data_frame(all_lectures)
    df_exercises = convert_data_to_data_frame(all_exercises)
    df_lectures_teacher = df_lectures[df_lectures["teacher_id"] == teacher_id]
    df_exercises_teacher = df_exercises[df_exercises["teacher_id"] == teacher_id]

    if df_lectures_teacher.empty and df_exercises_teacher.empty:
        print("No lectures or exercises found for the teacher saving empty report")
        df_complete_report = make_empty_personal_workload_report(teacher_id, teacher)
        return df_complete_report
    else:
        df_complete_report = make_personal_workload_report_with_data(
            teacher_id, teacher, df_lectures_teacher, df_exercises_teacher
        )
        return df_complete_report


def generate_summary_reports():
    all_teachers = get_all_teachers()
    all_lectures = get_all_lectures()
    all_exercises = get_all_exercises()
    df_teachers = convert_data_to_data_frame(all_teachers)
    df_lectures = convert_data_to_data_frame(all_lectures)
    df_exercises = convert_data_to_data_frame(all_exercises)
    df_concat_exercises_lectures = pd.concat([df_lectures, df_exercises])
    df_merge_with_teachers = pd.merge(
        df_concat_exercises_lectures,
        df_teachers,
        how="left",
        left_on="teacher_id",
        right_on="id",
    ).sort_values(by="name_x")
    # TODO need to fixed  to prepare report that validate with database model
    print(f"Generate summary report --- {df_merge_with_teachers}")
    return df_merge_with_teachers
