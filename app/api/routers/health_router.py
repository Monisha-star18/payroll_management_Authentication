from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_session)
):
    try:
        await db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "message": "PostgreSQL connection successful"
        }

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "PostgreSQL connection failed"
            }
        )