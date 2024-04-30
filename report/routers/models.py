from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class PersonalWorkloadReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    teacher: str
    hours_semester1: int
    hours_semester2: int
    pensum: int
    sum_hours: int
    difference_pensum_sum_hours: int


class SummaryClassesDepartmentReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    subject: str
    faculty: str
    study_year: int
    semester: int
    hours_lectures: int
    hours_exercises: int
    groups: int
    lecture_teacher: str
    exercise_teachers: int
    groups_for_teacher: int
    hours_for_teacher: int


class TeacherReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    teacher: str
    subject: str
    hours_lectures: int
    hours_exercises: int
    study_year: int
    semester: int


class ListTeacherReports(BaseModel):
    teacher_reports: List[TeacherReport]
