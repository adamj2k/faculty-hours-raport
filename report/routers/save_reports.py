import pandas as pd

from report.routers.database import (
    personal_workload_reports_collection,
    summary_reports_collection,
    teachers_reports_collection,
)
from report.routers.models import (
    PersonalWorkloadReport,
    SummaryClassesDepartmentReport,
    TeacherReport,
)


def save_teachers_report(report: pd.DataFrame):
    report_data = report.to_dict(orient="records")
    reports_to_save = [TeacherReport(**report) for report in report_data]
    teachers_reports_collection.insert_many(
        [report.saving_to_mongo() for report in reports_to_save]
    )


def save_personal_workload_report(report: pd.DataFrame):
    report_data = report.to_dict(orient="records")
    report_to_save = PersonalWorkloadReport(**report_data[0])
    personal_workload_reports_collection.insert_one(report_to_save.saving_to_mongo())


def save_summary_report(report: pd.DataFrame):
    report_data = report.to_dict(orient="records")
    print(f"Saving {report_data}")
    report_to_save = SummaryClassesDepartmentReport(**report_data[0])
    # TODO: finish after fix generate summary report function
    summary_reports_collection.insert_one(report_to_save.saving_to_mongo())
