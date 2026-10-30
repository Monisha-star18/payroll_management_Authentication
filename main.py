from fastapi import FastAPI

from app.api.routers.auth_router import router as auth_router
from app.api.routers.employee_salary_router import router as employee_salary_router
from app.api.routers.report_router import router as report_router

from app.core.exceptions.exception_handlers import register_exception_handlers

from app.core.logger import logger

app = FastAPI(title="Employee Payroll Management")

# Register all exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(employee_salary_router)
app.include_router(report_router)
app.include_router(auth_router)

logger.info("Payroll Management API configured")
