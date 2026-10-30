
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions.exceptions import AppException
from app.utilites.logger import logger


def register_exception_handlers(app: FastAPI):

    # 1. Our custom exceptions
    @app.exception_handler(AppException)
    async def custom_exception_handler(
        request: Request,
        exc: AppException
    ):
        log = (
            logger.error
            if exc.status_code >= 500
            else logger.warning
        )

        log(
            "%s | %s %s | %s",
            exc.status_code,
            request.method,
            request.url.path,
            exc.message
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": type(exc).__name__,
                "message": exc.message
            }
        )

    # 2. Existing FastAPI HTTPExceptions
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        logger.warning(
            "%s | %s %s | HTTP exception",
            exc.status_code,
            request.method,
            request.url.path
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )

    # 3. Pydantic / FastAPI validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        logger.warning(
            "422 | %s %s | Invalid request",
            request.method,
            request.url.path
        )

        return JSONResponse(
            status_code=422,
            content={
                "error": "ValidationError",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        )

    # 4. Unexpected exceptions
    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception
    ):
        logger.exception(
            "Unhandled error | %s %s",
            request.method,
            request.url.path
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "Internal server error"
            }
        )
