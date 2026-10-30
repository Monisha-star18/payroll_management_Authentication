from fastapi import FastAPI

from app.api.routers.auth_router import router as auth_router
from app.api.routers.employee_salary_router import router as employee_salary_router
from app.api.routers.report_router import router as report_router

from app.core.exceptions.exception_handlers import register_exception_handlers

from app.core.logger import logger
import time
from fastapi import Request

from app.core.logger import logger

app = FastAPI(title="Employee Payroll Management")

# Register all exception handlers
register_exception_handlers(app)


# Include routers
app.include_router(employee_salary_router)
app.include_router(report_router)
app.include_router(auth_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        "%s %s | Status: %s | Time: %.4f seconds",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response


logger.info("Payroll Management API configured")

