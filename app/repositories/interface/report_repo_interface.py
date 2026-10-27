from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.employee_salary_schema import EmployeeReportResponse


class EmployeeReportRepoInterface(ABC):

    @abstractmethod
    async def fetch_report(self,
        db:AsyncSession
        )->EmployeeReportResponse:
       pass

