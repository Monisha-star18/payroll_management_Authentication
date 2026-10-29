
import pytest

from app.services.implementation.payroll_services import PayrollService


@pytest.fixture
def payroll():
    return PayrollService()


# TEST 1: DA calculation
def test_calculate_da(payroll):
    result = payroll.calculate_da(20000)
    assert result == 2000


# TEST 2: PF calculation
def test_calculate_pf(payroll):
    result = payroll.calculate_pf(20000)
    assert result == 2400


# TEST 3: Gross salary
def test_calculate_gross_salary(payroll):
    result = payroll.calculate_gross_salary(20000)
    assert result == 22000


# TEST 4: Zero salary
def test_zero_salary(payroll):
    assert payroll.calculate_da(0) == 0
    assert payroll.calculate_pf(0) == 0
    assert payroll.calculate_gross_salary(0) == 0

