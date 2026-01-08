from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class Mongo:
    client: AsyncIOMotorClient | None = None


mongo = Mongo()


def get_client() -> AsyncIOMotorClient:
    if mongo.client is None:
        mongo.client = AsyncIOMotorClient(settings.mongodb_uri)
    return mongo.client


def get_db():
    client = get_client()
    return client[settings.mongodb_db]
