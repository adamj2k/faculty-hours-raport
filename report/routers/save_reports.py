from report.routers.database import (
    personal_workload_reports_collection,
    summary_reports_collection,
    teachers_reports_collection,
)


def save_teachers_report(report):
    teachers_reports_collection.insert_one(
        report.model_dump(by_alias=True, exclude=["id"])
    )


def save_personal_workload_report(report):
    personal_workload_reports_collection.insert_one(
        report.model_dump(by_alias=True, exclude=["id"])
    )


def save_summary_report(report):
    summary_reports_collection.insert_one(
        report.model_dump(by_alias=True, exclude=["id"])
    )
