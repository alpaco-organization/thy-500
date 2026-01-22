import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password


async def seed_admin():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]

    # Admin bilgileri
    admin_email = "admin@alpaco.com"
    admin_password = "alpacothy500"

    existing = await db.users.find_one({"email": admin_email})

    if existing:
        print(f"Admin zaten mevcut: {admin_email}")
        return

    admin_user = {
        "email": admin_email,
        "password_hash": hash_password(admin_password),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await db.users.insert_one(admin_user)

    print(f"Admin oluşturuldu!")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print(f"ID: {result.inserted_id}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
