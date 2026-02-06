import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password


async def seed_admin():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]

    admin_email = settings.admin_email
    admin_password = settings.admin_password

    existing = await db.users.find_one({"email": admin_email})

    admin_user = {
        "email": admin_email,
        "password_hash": hash_password(admin_password),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    if existing:
        # Update existing admin with new password
        result = await db.users.update_one(
            {"email": admin_email},
            {"$set": {
                "password_hash": hash_password(admin_password),
                "updated_at": datetime.utcnow()
            }}
        )
        print(f"Admin password updated!")
        print(f"Email: {admin_email}")
    else:
        # Create new admin
        result = await db.users.insert_one(admin_user)
        print(f"Admin created!")
        print(f"Email: {admin_email}")
        print(f"ID: {result.inserted_id}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_admin())
