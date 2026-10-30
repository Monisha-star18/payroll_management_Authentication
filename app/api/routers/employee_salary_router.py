from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependency.auth import require_roles
from app.api.dependency.dependency import get_all_services
from app.database.session import get_session
from app.schemas.employee_salary_schema import (
    CreateEmployeeSalary,
    DepartmentTotalResponse,
    EmployeeCreateResponse,
    EmployeeFullResponse,
    IncrementRequest,
    IncrementResponse,
    SalaryCreateResponse,
    CreateEmployeeWithEmail,
)

from app.services.implementation.employee_salary_service import EmployeeSalaryService

router = APIRouter(prefix="/api/employee_salary")

#post the new employee personal details 
#dependency injection
@router.post("/add_employee_deatils",
            response_model=EmployeeCreateResponse,
            dependencies=[Depends(require_roles("admin"))]
            )
async def add_employee_deatils( employee_details :CreateEmployeeWithEmail,
                               db:AsyncSession = Depends(get_session),
                               service:EmployeeSalaryService = Depends(get_all_services)
                               ):
    
    return await service.add_employee_personalDetails(employee_details,db)


#post the new employee salary details 
@router.post('/add_employee_salary_deatils',
            response_model=SalaryCreateResponse,
            dependencies=[Depends(require_roles("admin"))]
            )
async def create_employee_salary(employee_salary_deatils :CreateEmployeeSalary,
                                 db:AsyncSession = Depends(get_session),
                                 service:EmployeeSalaryService = Depends(get_all_services)
                                ):
    return await service.create_employee(employee_salary_deatils,db)

#get the employee deatils 
@router.get('/{employee_id}',
            response_model=EmployeeFullResponse,
            dependencies=[Depends(require_roles("admin", "user"))]
            )
async def get_all_employee_details(employee_id: int= Path(gt=0),
                                   db:AsyncSession = Depends(get_session),
                                   service:EmployeeSalaryService = Depends(get_all_services)
                                   ):
    return await service.get_all_employee(employee_id,db)


#increment by percentage
@router.post('/{employee_id}/increment',
            response_model=IncrementResponse,
            dependencies=[Depends(require_roles("admin"))]
            )
async def increase_employee_salary(employee_id: int , 
                                    increment_details: IncrementRequest,
                                    db: AsyncSession = Depends(get_session),
                                    service:EmployeeSalaryService = Depends(get_all_services)
                                    ):
    return await service.increase_salary(employee_id, increment_details, db)

#get department wise total salary
@router.get('/',
            response_model=list[DepartmentTotalResponse],
            dependencies=[Depends(require_roles("admin", "user"))]
            )
async def department_totals(db: AsyncSession = Depends(get_session),
                            service:EmployeeSalaryService = Depends(get_all_services)
                            ):
    return await service.get_department_totals(db)
