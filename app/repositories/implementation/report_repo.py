from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Employee_Details_Model import EmployeeDeatils
from app.repositories.interface.report_repo_interface import EmployeeReportRepoInterface
from app.schemas.employee_salary_schema import EmployeeReportResponse

class EmployeeReportRepo(EmployeeReportRepoInterface):

    async def fetch_report(self,
        db:AsyncSession
        )->EmployeeReportResponse:
        
        try:
            #Get total employee count
            stmt_tc = select(func.count()).select_from(EmployeeDeatils)
            result = await db.execute(stmt_tc)

            total_employee = result.scalar_one()

            #Get total female employee count
            stmt_twc = select(func.count()).select_from(EmployeeDeatils).where(EmployeeDeatils.gender == "Female")
            result = await db.execute(stmt_twc)

            total_women_employee = result.scalar_one()

            #Get total male employee count
            stmt_tmc = select(func.count()).select_from(EmployeeDeatils).where(EmployeeDeatils.gender == "Male")
            result = await db.execute(stmt_tmc)

            total_men_employee = result.scalar_one()

            #get department having cout more than 2 employees 
            stmt_tcd = select(EmployeeDeatils.department, 
                              func.count().label("employee_count")
                            ) .group_by(EmployeeDeatils.department) . having(func.count() > 2)
            
            result = await db.execute(stmt_tcd)
            department_counts = result.all()

            
            departments = [
                            { "department": row.department, "employee_count": row.employee_count }
                            for row in department_counts
                        ]

            #Return the report
            return {"total_employee_count" : total_employee ,
                    "total_women_employee_count" : total_women_employee,
                    "total_Men_employee_count" : total_men_employee,
                     "departments_with_more_than_2_employees": departments}
            
        except SQLAlchemyError as er:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(er))
            

