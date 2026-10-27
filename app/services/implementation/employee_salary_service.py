from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Employee_Salary_Model import EmployeePayDeatils
from app.repositories.interface.employee_salary_interface import EmployeeSalaryRepoInterface
from app.schemas.employee_salary_schema import CreateEmployeeDetails, CreateEmployeeSalary, DepartmentTotalResponse, EmployeeCreateResponse, EmployeeFullResponse, IncrementRequest, SalaryComponents, SalaryCreateResponse
from app.services.interface.payroll_services_interface import PayrollServiceInterface


class EmployeeSalaryService:

    def __init__(self,
        payroll_services:PayrollServiceInterface,
        employee_repository:EmployeeSalaryRepoInterface
        )->None:
        
        self.payroll_services = payroll_services
        self.employee_repository=employee_repository
      
    #the payroll calculations 
    def payroll_calutaions(self,
        basic_salary:float
        )->SalaryComponents:
            
            da = self.payroll_services.calculate_da(basic_salary)

            pf=self.payroll_services.calculate_pf(basic_salary)

            gross_salary=self.payroll_services.calculate_gross_salary(basic_salary)
            
            salary_deatils = {"da":da , 
                                "pf":pf,
                                "gross_salary":gross_salary}
    
            return salary_deatils


    async def add_employee_personalDetails(self,
        employee_details:CreateEmployeeDetails,
        db:AsyncSession
        ) -> EmployeeCreateResponse:

        return await self.employee_repository.post_employee_personalDetails(employee_details,db)


    #post new employees
    async def create_employee(self,
        employee_salary_deatils:CreateEmployeeSalary,
        db:AsyncSession
        )->SalaryCreateResponse:

        #change the object to dict
        employee_deatils = employee_salary_deatils.model_dump()

        basic_salary = employee_deatils["basic_salary"]

        salary_deatils = self.payroll_calutaions(basic_salary)

        employee_compailed_deatils = {**employee_deatils,**salary_deatils}

        return await self.employee_repository.post_employee(employee_compailed_deatils,db)

  
    # #get all employees
    async def get_all_employee(self,
        employee_id:int,
        db:AsyncSession
        )->EmployeeFullResponse:

        return await self.employee_repository.fetch_all_employee_salary(employee_id,db)

    # #increament
    async def increase_salary(self, 
        employee_id: int,
        increment_details:IncrementRequest, 
        db: AsyncSession
        ) -> EmployeePayDeatils:
        
        return await self.employee_repository.increase_salary(employee_id, increment_details.percent, db)

    #get department totals 
    async def get_department_totals(self, 
        db: AsyncSession
        )->list[DepartmentTotalResponse]:
        
        return await self.employee_repository.fetch_department_totals(db)


