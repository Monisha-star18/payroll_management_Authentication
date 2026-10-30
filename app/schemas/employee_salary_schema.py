import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

BASIC_SALARY = dict(gt=5_000,lt=1_000_000)
GENDER = Literal["Male", "Female", "Other"]     
DEPARTMENT = Literal["IT","HR","Finance"]

class Base(BaseModel):
    pass

#general salary body 
class EmployeeSalaryResponse(Base):

    model_config = ConfigDict(from_attributes=True)
    
    employee_id: int
    basic_salary: float
    da: float
    pf: float
    gross_salary: float

#create a new employee with personal details 
class CreateEmployeeDetails(Base):
    model_config = ConfigDict(extra='forbid')

    employee_id: int = Field(ge=1)
    employee_name: str = Field(min_length=2, max_length=50,default="")
    gender: GENDER = Field(default="")
    department :DEPARTMENT= Field(default="")



#create a new employee with salary details 
class CreateEmployeeSalary(Base):
    model_config = ConfigDict(extra='forbid')

    employee_id :int = Field(ge=1)
    basic_salary : float = Field(**BASIC_SALARY)

#for the increment 
class IncrementRequest(Base):
    model_config = ConfigDict(extra='forbid')

    percent : float = Field(gt=0,le=100) 

#for the increament response body 
class IncrementResponse(Base):
    message: str
    details: EmployeeSalaryResponse | None = None

#for the department wise total salary
class DepartmentTotalResponse(Base):
    department: str
    Department_total_salary: float

class EmployeeCreateResponse(Base):
    message: str
    Employee_details: CreateEmployeeDetails

#da, pf and gross salary calculated by the payroll service
class SalaryComponents(Base):
    da: float
    pf: float
    gross_salary: float

#internal: the full salary row (input + calculated values) that goes to the repo
class SalaryRecord(Base):
    employee_id: int
    basic_salary: float
    da: float
    pf: float
    gross_salary: float

#response body after creating the salary details
class SalaryCreateResponse(Base):
    message: str
    Salary_deatiles: SalaryRecord

#employee personal details + salary details (salary is None if not added yet)
class EmployeeFullResponse(Base):
    employee_id: int
    employee_name: str
    gender: str
    department: str
    employee_salary: float | None = None
    da: float | None = None
    pf: float | None = None
    employee_gross_salary: float | None = None

class DepartmentTotalResponse(Base):
    department: str
    Department_total_salary: float

#employee count for one department
class DepartmentCountResponse(Base):
    department: str
    employee_count: int

#the full employee report
class EmployeeReportResponse(Base):
    total_employee_count: int
    total_women_employee_count: int
    total_Men_employee_count: int
    departments_with_more_than_2_employees: list[DepartmentCountResponse]

class CreateEmployeeWithEmail(CreateEmployeeDetails):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:

        value = value.strip()

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid email address")

        return value

class EmployeeCreateResponse(Base):
    message: str
    Employee_details: CreateEmployeeDetails
    email_sent: bool