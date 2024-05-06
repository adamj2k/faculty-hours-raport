from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from .database import reports_collection
from .models import ListTeacherReports  # noqa
from .models import TeacherReport  # noqa
from .models import TeacherReportCreateResponse  # noqa; noqa

router = APIRouter()


@router.get("/teacher-reports-list", response_model=ListTeacherReports)
async def read_reports():
    return ListTeacherReports(
        teacher_reports=await reports_collection.find().to_list(1000)
    )


@router.get("/teacher-report/{id}", response_model=TeacherReport)
async def read_teacher_report(id: str):
    teacher_report = await reports_collection.find_one({"_id": ObjectId(id)})
    if teacher_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )
    return teacher_report


@router.post("/teacher-report/create/", response_model=TeacherReportCreateResponse)
async def create_teacher_report(teacher_report: TeacherReport):
    new_report = await reports_collection.insert_one(
        teacher_report.model_dump(by_alias=True, exclude=["id"])
    )
    created_report = await reports_collection.find_one({"_id": new_report.inserted_id})
    return created_report


@router.delete("/teacher-report/delete/{id}", response_model=TeacherReport)
async def delete_teacher_report(id: str):
    deleted_report = await reports_collection.find_one_and_delete({"_id": ObjectId(id)})
    if deleted_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
