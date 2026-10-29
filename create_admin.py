import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import select

from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.User_Model import User

load_dotenv()

admin__password = os.getenv("ADMIN_PASSWORD")

async def main():
    async with SessionLocal() as db:
        existing = await db.execute(select(User).where(User.username == "admin"))
        if existing.scalar_one_or_none():
            print("admin already exists")
            return
        db.add(User(username="admin", hashed_password=hash_password(admin__password), role="admin"))
        await db.commit()
        print("admin created")

asyncio.run(main())