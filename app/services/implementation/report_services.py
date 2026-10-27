from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interface.report_repo_interface import EmployeeReportRepoInterface
from app.schemas.employee_salary_schema import EmployeeReportResponse


class EmployeeReport:

        def __init__(self,
                report_repo:EmployeeReportRepoInterface
                )->None:
                
                self.report_repo=report_repo

        async def get_report(self,
                db:AsyncSession
                )-> EmployeeReportResponse :
                
                return await self.report_repo.fetch_report(db)

