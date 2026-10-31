import razorpay

from fastapi import APIRouter, HTTPException

from app.services.implementation.razorpay_service import (
    create_razorpay_order
)

router = APIRouter(
    prefix="/api/razorpay",
    tags=["Razorpay"]
)


@router.post("/create-order")
async def create_order():
    try:
        return await create_razorpay_order()

    except razorpay.errors.BadRequestError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay order request"
        )

    except razorpay.errors.ServerError:
        raise HTTPException(
            status_code=502,
            detail="Razorpay server error"
        )