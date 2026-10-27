from fastapi import FastAPI

from app.routers.employee_salary_router import router as employee_salary_router
from app.routers.report_router import router as report_router
from app.routers.auth_router import router as auth_router

app=FastAPI(title="Employee Payroll Management")

app.include_router(employee_salary_router)
app.include_router(report_router)
app.include_router(auth_router)
