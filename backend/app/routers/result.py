from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.db.mongo import get_db
from app.models.result import ResultOut, ResultCreate

router = APIRouter(prefix="/api/results", tags=["results"])


# Create new result (saves to results + updates persons)
@router.post("/", response_model=ResultOut)
async def create_result(result: ResultCreate):
    db = get_db()
    results_collection = db["results"]
    persons_collection = db["persons"]
    
    # 1. Save to results (new record every time)
    result_data = {
        "resultId": str(uuid.uuid4()),
        "personId": result.personId,
        "personName": result.personName,
        "matchCorrect": result.matchCorrect,
        "feedback": result.feedback,
        "createdAt": datetime.now()
    }
    
    await results_collection.insert_one(result_data)
    
    # 2. Update persons (latest value)
    await persons_collection.update_one(
        {"personId": result.personId},
        {
            "$set": {
                "matchCorrect": result.matchCorrect,
                "feedback": result.feedback
            }
        }
    )
    
    return ResultOut(**result_data)


# Get all results
@router.get("/", response_model=List[ResultOut])
async def get_all_results():
    db = get_db()
    collection = db["results"]
    
    cursor = collection.find({}, projection={"_id": 0})
    results = await cursor.to_list(length=1000)
    
    return results


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