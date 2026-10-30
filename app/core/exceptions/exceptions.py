
#base exception class 
class AppException(Exception):
    def __init__(self,message: str,status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class EmployeeNotFoundException(AppException):
    def __init__(self, employee_id: int):
        super().__init__(
            message=f"Employee {employee_id} not found",
            status_code=404
        )


class EmployeeAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="Employee already exists",
            status_code=409
        )


class SalaryAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="Salary details already exist",
            status_code=409
        )


class EmployeeNotRegisteredException(AppException):
    def __init__(self):
        super().__init__(
            message="Employee is not registered",
            status_code=404
        )


class DatabaseOperationException(AppException):
    def __init__(self):
        super().__init__(
            message="Database operation failed",
            status_code=500
        )
