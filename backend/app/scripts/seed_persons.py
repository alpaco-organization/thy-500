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
    """Load sample data from persons_mapped.json file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Use /app path in Docker, otherwise use script directory
    if os.path.exists("/app/app/scripts/datas/mapped_data/persons_mapped.json"):
        json_path = "/app/app/scripts/datas/mapped_data/persons_mapped.json"
    else:
        json_path = os.path.join(script_dir, "datas", "mapped_data", "persons_mapped.json")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_unique_id(existing_ids: set[str], prefix: str = "DUP_") -> str:
    """Generate a unique ID that doesn't exist in the set."""
    counter = 1
    while True:
        new_id = f"{prefix}{counter:06d}"
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id
        counter += 1


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
    print(f"Loaded {len(sample)} records from JSON")

    # Log records with empty personId
    empty_ids = [doc for doc in sample if not doc.get("personId")]
    print(f"Records with empty personId: {len(empty_ids)}")
    for doc in empty_ids[:5]:
        print(f"  - {doc.get('name')}")

    # Collect all existing personIds to detect duplicates
    all_person_ids: set[str] = set()
    for doc in sample:
        all_person_ids.add(doc.get("personId", ""))

    # Also get existing IDs from database
    existing_cursor = persons.find({}, {"personId": 1})
    async for existing_doc in existing_cursor:
        all_person_ids.add(existing_doc.get("personId", ""))

    # Track seen IDs to detect duplicates within the JSON
    seen_ids: set[str] = set()
    duplicates_reassigned = 0

    upserts = 0
    updates = 0
    for doc in sample:
        person_id = doc.get("personId", "")

        # If this personId was already seen, assign a new unique ID
        if person_id in seen_ids or not person_id:
            new_id = _generate_unique_id(all_person_ids)
            doc["personId"] = new_id
            doc["original_personId"] = person_id  # Keep track of original
            duplicates_reassigned += 1
        else:
            seen_ids.add(person_id)

        if "name" in doc:
            doc["name_normalized"] = normalize_name(str(doc["name"]))
        res = await persons.update_one(
            {"personId": doc["personId"]},
            {"$set": doc},
            upsert=True,
        )
        if res.upserted_id is not None:
            upserts += 1
        elif res.modified_count > 0:
            updates += 1

    total = await persons.count_documents({})
    print(f"Seed complete. Upserted {upserts}, Updated {updates}, Duplicates reassigned {duplicates_reassigned}. persons total={total}. DB={db_name}")

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
