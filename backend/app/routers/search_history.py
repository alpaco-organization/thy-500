from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.db.mongo import get_db
from app.models.search_history import SearchHistoryOut, SearchHistoryCreate

router = APIRouter(prefix="/api/search-history", tags=["search-history"])


async def log_search(
    search_type: str,
    query: str,
    person_id: str | None = None,
    person_name: str | None = None,
    found: bool = False,
) -> None:
    """Log a search to the search history collection."""
    db = get_db()
    collection = db["search_history"]

    search_data = {
        "searchId": str(uuid.uuid4()),
        "searchType": search_type,
        "query": query,
        "personId": person_id,
        "personName": person_name,
        "found": found,
        "createdAt": datetime.now(),
    }

    await collection.insert_one(search_data)


@router.get("/", response_model=List[SearchHistoryOut])
async def get_all_search_history():
    """Get all search history records, ordered by most recent first."""
    db = get_db()
    collection = db["search_history"]

    cursor = collection.find({}, projection={"_id": 0}).sort("createdAt", -1)
    results = await cursor.to_list(length=1000)

    return results


@router.get("/recent", response_model=List[SearchHistoryOut])
async def get_recent_searches(limit: int = 50):
    """Get recent search history records."""
    db = get_db()
    collection = db["search_history"]

    cursor = collection.find({}, projection={"_id": 0}).sort("createdAt", -1).limit(limit)
    results = await cursor.to_list(length=limit)

    return results


@router.get("/by-query/{query}", response_model=List[SearchHistoryOut])
async def get_searches_by_query(query: str):
    """Get all searches matching a specific query string."""
    db = get_db()
    collection = db["search_history"]

    cursor = collection.find(
        {"query": {"$regex": query, "$options": "i"}},
        projection={"_id": 0}
    ).sort("createdAt", -1)
    results = await cursor.to_list(length=100)

    return results


@router.delete("/")
async def clear_search_history():
    """Clear all search history."""
    db = get_db()
    collection = db["search_history"]

    result = await collection.delete_many({})

    return {"deleted_count": result.deleted_count}
