from datetime import datetime
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

    def saving_to_mongo(self):
        return dict(self)


class ListPersonalWorkloadReport(BaseModel):
    personal_workload_report: List[PersonalWorkloadReport]


class PersonalWorkloadReportCreateResponse(BaseModel):
    created: PersonalWorkloadReport
    timestamp: datetime


class Teacher(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    teacher_name: str
    lecture_teacher: bool
    exercise_teachers: bool
    groups_for_teacher: int
    hours_for_teacher: int

    def saving_to_mongo(self):
        return dict(self)


class SummaryClassesDepartmentReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    subject: str
    faculty: str
    study_year: int
    semester: int
    hours_lectures: int
    hours_exercises: int
    groups: int
    teachers: List[Teacher]

    def saving_to_mongo(self):
        return dict(self)


class ListSummaryClassesDepartmentReport(BaseModel):
    summary_classes_department_report: List[SummaryClassesDepartmentReport]


class SummaryClassesDepartmentReportCreateResponse(BaseModel):
    created: SummaryClassesDepartmentReport
    timestamp: datetime


class TeacherReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    teacher: str
    subject: str
    hours_lectures: int
    hours_exercises: int
    study_year: int
    semester: int

    def saving_to_mongo(self):
        return dict(self)


class ListTeacherReports(BaseModel):
    teacher_reports: List[TeacherReport]


class TeacherReportCreateResponse(BaseModel):
    created: TeacherReport
    timestamp: datetime
