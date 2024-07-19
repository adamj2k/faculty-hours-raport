import io
import json

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
)


def generate_teachers_reports():
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
    try:
        teacher = get_teacher(teacher_id)
        all_lectures = get_all_lectures()
        all_exercises = get_all_exercises()
        df_lectures = pd.read_json(
            io.StringIO(json.dumps(all_lectures)), orient="records"
        )
        df_exercises = pd.read_json(
            io.StringIO(json.dumps(all_exercises)), orient="records"
        )
        df_lectures_teacher = df_lectures[df_lectures["teacher_id"] == teacher_id]
        df_exercises_teacher = df_exercises[df_exercises["teacher_id"] == teacher_id]

        if df_lectures_teacher.empty and df_exercises_teacher.empty:
            print("No lectures or exercises found for the teacher saving empty report")
            df_complete_report = pd.DataFrame(
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
            return df_complete_report
        else:
            df_join_lectures_exercises = pd.concat(
                [df_lectures_teacher, df_exercises_teacher]
            )
            df_semesters = df_join_lectures_exercises.groupby(
                "semester", as_index=False
            ).sum()
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
                df_complete_report["hours_semester1"]
                + df_complete_report["hours_semester2"]
            )
            df_complete_report["difference_pensum_sum_hours"] = (
                df_complete_report["pensum"] - df_complete_report["sum_hours"]
            )
            return df_complete_report
    except Exception as error:
        print(f"Generate personal workload report ERROR --- {error}")


def generate_summary_reports():
    try:
        all_teachers = get_all_teachers()
        all_lectures = get_all_lectures()
        all_exercises = get_all_exercises()
        df_teachers = pd.read_json(
            io.StringIO(json.dumps(all_teachers)), orient="records"
        )
        df_lectures = pd.read_json(
            io.StringIO(json.dumps(all_lectures)), orient="records"
        )
        df_exercises = pd.read_json(
            io.StringIO(json.dumps(all_exercises)), orient="records"
        )
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
    except Exception as error:
        print(f"Generate summary report ERROR--- {error}")
