import asyncio
import uuid
import razorpay

from app.core.config import get_settings


async def create_razorpay_order():
    settings = get_settings()

    client = razorpay.Client(
        auth=(
            settings.razorpay_key_id,
            settings.razorpay_key_secret
        )
    )

    order_data = {
        "amount": 10000,
        "currency": "INR",
        "receipt": "order_" + uuid.uuid4().hex[:20]
    }

    order = await asyncio.to_thread(
        client.order.create,
        data=order_data
    )

    return order