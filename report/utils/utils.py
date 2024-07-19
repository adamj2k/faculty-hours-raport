import io
import json
import re

import pandas as pd


def find_teacher_id_in_body(body):
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
