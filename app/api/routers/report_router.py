from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.api.dependency.auth import require_roles
from app.api.dependency.dependency import get_all_report_services
from app.schemas.employee_salary_schema import EmployeeReportResponse
from app.services.implementation.report_services import EmployeeReport


router = APIRouter(prefix="/api/report",tags=["Report"])

@router.get('/',
            response_model=EmployeeReportResponse,
            dependencies=[Depends(require_roles("admin", "user"))]
            )
async def get_employee_report(db:AsyncSession = Depends(get_session),
                              service : EmployeeReport = Depends(get_all_report_services),
                            ):
    return await service.get_report(db)