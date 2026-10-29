
import pytest
from pydantic import ValidationError

from app.schemas.employee_salary_schema import (
    CreateEmployeeSalary,
    CreateEmployeeDetails,
    IncrementRequest,
)


def test_valid_salary():
    salary = CreateEmployeeSalary(
        employee_id=1,
        basic_salary=25000
    )
    assert salary.basic_salary == 25000


@pytest.mark.parametrize(
    "amount",
    [0, -1000, 5000, 1000000]
)
def test_invalid_salary(amount):
    with pytest.raises(ValidationError):
        CreateEmployeeSalary(
            employee_id=1,
            basic_salary=amount
        )


def test_valid_increment():
    request = IncrementRequest(percent=10)
    assert request.percent == 10


@pytest.mark.parametrize(
        "percent", 
        [-5, 0, 101]
)
def test_invalid_increment(percent):
    with pytest.raises(ValidationError):
        IncrementRequest(percent=percent)


def test_invalid_employee_id():
    with pytest.raises(ValidationError):
        CreateEmployeeDetails(
            employee_id=0,
            employee_name="Test Employee",
            gender="Female",
            department="IT"
        )


def test_invalid_department():
    with pytest.raises(ValidationError):
        CreateEmployeeDetails(
            employee_id=1,
            employee_name="Test Employee",
            gender="Female",
            department="Sales"
        )
