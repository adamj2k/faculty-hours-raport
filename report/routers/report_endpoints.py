from bson import ObjectId
from fastapi import APIRouter, status
from fastapi.responses import Response

from report.models.database import (
    personal_workload_reports_collection,
    teachers_reports_collection,
)
from report.models.models import (
    ListPersonalWorkloadReport,
    ListTeacherReports,
    PersonalWorkloadReport,
    PersonalWorkloadReportCreateResponse,
    TeacherReport,
    TeacherReportCreateResponse,
)
from report.routers.exceptions import FeatureNotFindException

router = APIRouter()


@router.get("/teacher-reports/list", response_model=ListTeacherReports)
async def read_reports():
    return ListTeacherReports(
        teacher_reports=await teachers_reports_collection.find().to_list(1000)
    )


@router.get("/teacher-report/{id}", response_model=TeacherReport)
async def read_teacher_report(id: str):
    teacher_report = await teachers_reports_collection.find_one({"_id": ObjectId(id)})
    if teacher_report is None:
        raise FeatureNotFindException
    return teacher_report


@router.post("/teacher-report/create/", response_model=TeacherReportCreateResponse)
async def create_teacher_report(teacher_report: TeacherReport):
    new_report = await teachers_reports_collection.insert_one(
        teacher_report.model_dump(by_alias=True, exclude=["id"])
    )
    created_report = await teachers_reports_collection.find_one(
        {"_id": new_report.inserted_id}
    )
    return created_report


@router.delete("/teacher-report/delete/{id}", response_model=TeacherReport)
async def delete_teacher_report(id: str):
    deleted_report = await teachers_reports_collection.find_one_and_delete(
        {"_id": ObjectId(id)}
    )
    if deleted_report is None:
        raise FeatureNotFindException
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/personal-workload-report/list", response_model=ListPersonalWorkloadReport)
async def read_personal_workload_report():
    return ListPersonalWorkloadReport(
        personal_workload_report=await personal_workload_reports_collection.find().to_list(
            1000
        )
    )


@router.get("/personal-workload-report/{id}", response_model=PersonalWorkloadReport)
async def read_personal_workload_report(id: str):
    personal_workload_report = await personal_workload_reports_collection.find_one(
        {"_id": ObjectId(id)}
    )
    if personal_workload_report is None:
        raise FeatureNotFindException
    return personal_workload_report


@router.post(
    "/personal-workload-report/create/",
    response_model=PersonalWorkloadReportCreateResponse,
)
async def create_personal_workload_report(
    personal_workload_report: PersonalWorkloadReport,
):
    new_personal_workload_report = (
        await personal_workload_reports_collection.insert_one(
            personal_workload_report.model_dump(by_alias=True, exclude=["id"])
        )
    )
    created_personal_workload_report = (
        await personal_workload_reports_collection.find_one(
            {"_id": new_personal_workload_report.inserted_id}
        )
    )
    return created_personal_workload_report
