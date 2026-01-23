import asyncio
import json
import os
import sys
from typing import Any

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


def _load_sample_data() -> list[dict[str, Any]]:
    """Load sample data from location_data.json file."""
    # Look for location_data.json in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = "/app/app/scripts/datas/mapped_data/persons_mapped.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def main() -> None:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/thy500")
    db_name = _mongo_db_name_from_uri(mongo_uri)

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    persons = db["persons"]

    # Ensure the unique index exists (matches app startup behavior)
    await persons.create_index("personId", unique=True)

    # Load sample data from JSON file
    sample = _load_sample_data()

    upserts = 0
    for doc in sample:
        if "name" in doc:
            doc["name_normalized"] = normalize_name(str(doc["name"]))
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