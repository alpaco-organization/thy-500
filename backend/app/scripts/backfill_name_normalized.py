import asyncio
import os
import sys

from motor.motor_asyncio import AsyncIOMotorClient

_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _APP_ROOT not in sys.path:
    sys.path.insert(0, _APP_ROOT)

from app.utils.normalize import normalize_name


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

    cursor = persons.find(
        {
            "name": {"$exists": True, "$type": "string"},
            "$or": [
                {"name_normalized": {"$exists": False}},
                {"name_normalized": None},
                {"name_normalized": ""},
            ],
        },
        projection={"_id": 1, "name": 1},
    )

    updated = 0
    async for doc in cursor:
        name = doc.get("name")
        if not name:
            continue

        await persons.update_one(
            {"_id": doc["_id"]},
            {"$set": {"name_normalized": normalize_name(name)}},
        )
        updated += 1
        if updated % 1000 == 0:
            print(f"Updated {updated} docs...")

    print(f"Done. Updated {updated} docs. DB={db_name}")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
