import asyncio
import os
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient


def _mongo_db_name_from_uri(uri: str) -> str:
    # Prefer explicit DB name if present in URI path, else fall back.
    # Example: mongodb://mongo:27017/thy500
    try:
        path = uri.split("?", 1)[0].split("//", 1)[1].split("/", 1)[1]
    except Exception:
        path = ""
    db = (path or "").strip("/")
    return db or os.getenv("MONGO_DB", "thy500")


async def main() -> None:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/thy500")
    db_name = _mongo_db_name_from_uri(mongo_uri)

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    persons = db["persons"]

    # Ensure the unique index exists (matches app startup behavior)
    await persons.create_index("personId", unique=True)

    sample: list[dict[str, Any]] = [
        {"personId": "1001", "name": "Mehmet Gökalp Köreken", "x": 45508, "y": 10150},
        {"personId": "1002", "name": "Mert Yıldırım", "x": 45508, "y": 14825},
        {"personId": "1003", "name": "Alpaco Team", "x": 45508, "y": 15991},
        {"personId": "1004", "name": "Elif Sude Aslan", "x": 45508, "y": 17160},
        {"personId": "1005", "name": "Zeynep Aydin", "x": 45512, "y": 10153},
    ]

    upserts = 0
    for doc in sample:
        res = await persons.update_one(
            {"personId": doc["personId"]},
            {"$set": doc},
            upsert=True,
        )
        if res.upserted_id is not None:
            upserts += 1

    total = await persons.count_documents({})
    print(f"Seed complete. Upserted {upserts} docs. persons total={total}. DB={db_name}")

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
