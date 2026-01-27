from fastapi import APIRouter, HTTPException, Response, Query
from typing import List, Optional
import uuid
import unicodedata
from datetime import datetime

from app.db.mongo import get_db
from app.models.result import ResultOut, ResultCreate

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/")
async def create_result(result: ResultCreate):
    db = get_db()
    results_collection = db["results"]
    persons_collection = db["persons"]

    if result.feedback is None:
        raise HTTPException(
            status_code=400,
            detail="Feedback must be provided"
        )

    result_data = {
        "resultId": str(uuid.uuid4()),
        "personId": result.personId,
        "personName": result.personName,
        "feedback": result.feedback,
        "createdAt": datetime.now()
    }

    await results_collection.insert_one(result_data)

    await persons_collection.update_one(
        {"personId": result.personId},
        {"$set": {"feedback": result.feedback}}
    )

    return {}

# Get all results with pagination and search
@router.get("/")
async def get_all_results(page: int = 0, search: Optional[str] = None):
    db = get_db()
    collection = db["results"]

    page_size = 30
    skip = page * page_size

    query = {}
    if search:
        search_upper = search.translate(str.maketrans("iışğüçö", "İIŞĞÜÇÖ")).upper()
        search_upper = unicodedata.normalize("NFD", search_upper)
        query = {
            "$or": [
                {"personId": {"$regex": search_upper}},
                {"personName": {"$regex": search_upper}}
            ]
        }

    total = await collection.count_documents(query)
    total_pages = (total + page_size - 1) // page_size

    cursor = collection.find(query, projection={"_id": 0}).sort("createdAt", -1).skip(skip).limit(page_size)
    results = await cursor.to_list(length=page_size)

    return {
        "data": results,
        "page": page,
        "totalPages": total_pages,
        "total": total
    }


# Get results by personId
@router.get("/by-person/{person_id}", response_model=List[ResultOut])
async def get_results_by_person(person_id: str):
    db = get_db()
    collection = db["results"]
    
    cursor = collection.find(
        {"personId": person_id},
        projection={"_id": 0}
    )
    results = await cursor.to_list(length=100)
    
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    
    return results