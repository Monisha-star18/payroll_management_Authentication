from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.employee_salary_schema import CreateEmployeeDetails, DepartmentTotalResponse, EmployeeCreateResponse, EmployeeFullResponse, IncrementResponse, SalaryCreateResponse, SalaryRecord



class EmployeeSalaryRepoInterface(ABC):

    @abstractmethod
    async def post_employee_personalDetails(self, 
        employee_details: CreateEmployeeDetails, 
        db: AsyncSession
        )->EmployeeCreateResponse:

        pass

    @abstractmethod
    async def post_employee(self, 
        employee_details: SalaryRecord,
        db: AsyncSession
        )-> SalaryCreateResponse:
        pass

    @abstractmethod
    async def fetch_all_employee_salary(self, 
        employee_id: int, 
        db: AsyncSession
        )-> EmployeeFullResponse:
        pass

    @abstractmethod
    async def increase_salary(self, 
        employee_id: int, 
        percent: float, 
        db: AsyncSession
        )-> IncrementResponse:
        pass

    @abstractmethod
    async def fetch_department_totals(self, 
        db: AsyncSession
        )->list[DepartmentTotalResponse]:
        pass
        
