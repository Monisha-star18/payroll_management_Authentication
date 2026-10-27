from decimal import Decimal
from fastapi import HTTPException,Depends
from sqlalchemy import func, select,text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.models.Employee_Details_Model import EmployeeDeatils
from app.models.Employee_Salary_Model import EmployeePayDeatils
from app.repositories.interface.employee_salary_interface import EmployeeSalaryRepoInterface
from app.schemas.employee_salary_schema import CreateEmployeeDetails, DepartmentTotalResponse, EmployeeCreateResponse, EmployeeFullResponse, IncrementResponse, SalaryCreateResponse, SalaryRecord


class EmployeeSalaryRepo(EmployeeSalaryRepoInterface):

    def __init__(self):
        pass

    #add employee perosnal deatils 
    async def post_employee_personalDetails(self, 
        employee_personal_details: CreateEmployeeDetails, 
        db: AsyncSession
        )->EmployeeCreateResponse:
    
        try:
            employee_details = employee_personal_details.model_dump()

            employee_personal_data = EmployeeDeatils(**employee_details)

            db.add(employee_personal_data)
            await db.commit()

            return{"message":f"Employee with ID {employee_details["employee_id"]} is added" , 
                    "Employee_details":employee_details}

        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Employee ID already exists")
        
        except SQLAlchemyError as er:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(er))

    #add new employess salary details 
    async def post_employee(self, 
        employee_details: SalaryRecord,
        db: AsyncSession
        )-> SalaryCreateResponse:
        
        try:
            employee_data = EmployeePayDeatils(**employee_details)
            db.add(employee_data)
            await db.commit()

            return{"message":f"Employee with ID {employee_details["employee_id"]} is added" , 
                   "Salary_deatiles":employee_details}
       
        except IntegrityError as er:
            await db.rollback()
            
            orig = er.orig
            error_type = type(orig).__name__

            if error_type == "ForeignKeyViolationError":
                raise HTTPException(  status_code=404,  detail="Employee is not registered.") from er

            elif error_type == "UniqueViolationError":
                raise HTTPException( status_code=409, detail="Salary details already exist.") from er

            else:
                raise HTTPException(status_code=400,detail="Database integrity constraint violation.") from er

        except SQLAlchemyError as er:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(er))
            

    #get  employees  by id 
    async def fetch_all_employee_salary(self, 
        employee_id: int, 
        db: AsyncSession
        )-> EmployeeFullResponse:

        try:
            employee =await db.get(EmployeeDeatils,employee_id, 
                                   options=[joinedload(EmployeeDeatils.salary)]
                                )
            
            if employee is None :
                raise HTTPException(status_code=404,
                                detail=f"Employee {employee_id} not found")
            basic = None
            gross_salary = None
            da = None
            pf = None

            if employee.salary is not None:
                basic = employee.salary.basic_salary
                da = employee.salary.da
                pf=employee.salary.pf
                gross_salary = employee.salary.gross_salary 


            employee_deatils = {
                "employee_id": employee.employee_id,
                "employee_name": employee.employee_name,
                "gender": employee.gender,
                "department":employee.department
            }

            employee_salary_details = {
                "employee_salary":basic,
                "da":da,
                "pf":pf,
                "employee_gross_salary":gross_salary
            }

            return {**employee_deatils,**employee_salary_details}

            
        except SQLAlchemyError as er:
            raise HTTPException(status_code=500, detail=str(er))

    #Increment by percentage  using store procedure 
    async def increase_salary(self, 
        employee_id: int, 
        percent: float, 
        db: AsyncSession
        )-> IncrementResponse:

        try:
            employee = await db.get(EmployeePayDeatils, employee_id)

            if employee is None:
                return {"message":f"The id {employee_id} dont exists ", "details": None}  
                           

            await db.execute(
                text("CALL sp_increase_salary(:employee_id, :percent)"),
                {"employee_id": employee_id, "percent": Decimal(str(percent))},
            )

            await db.commit()
            await db.refresh(employee)                   
            return {"message":"Increment updates","details":employee}

        except SQLAlchemyError as er:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(er))

    #get department wise salary 
    async def fetch_department_totals(self, 
        db: AsyncSession
        )->list[DepartmentTotalResponse]:
        
        try:
            stmt = (
                select (EmployeeDeatils.department,
                        func.sum(EmployeePayDeatils.basic_salary).label("total_salary")
                        )
                .join(EmployeeDeatils.salary)
                .group_by(EmployeeDeatils.department)
                .order_by(EmployeeDeatils.department)
                )

            result = (await db.execute(stmt)).all()

            return [
                {"department": row.department, "Department_total_salary": float(row.total_salary) }  for row in result 
            ]
        
        except SQLAlchemyError as er:
            raise HTTPException(status_code=500, detail=str(er))
        
