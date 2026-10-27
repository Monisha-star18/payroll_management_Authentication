from app.repositories.implementation.employee_salary_repo import EmployeeSalaryRepo
from app.repositories.implementation.report_repo import EmployeeReportRepo
from app.services.implementation.employee_salary_service import EmployeeSalaryService
from app.services.implementation.payroll_services import PayrollService
from app.services.implementation.report_services import EmployeeReport
from app.repositories.implementation.user_repo import UserRepo
from app.services.implementation.auth_service import AuthService


def get_all_services()->EmployeeSalaryService:

    payroll_cal = PayrollService()
    
    repository = EmployeeSalaryRepo()

    services = EmployeeSalaryService(payroll_cal,repository)

    return services 

def get_all_report_services()->EmployeeReport:

    repository = EmployeeReportRepo()

    service = EmployeeReport(repository)

    return service

def get_auth_service() -> AuthService:
    return AuthService(UserRepo())