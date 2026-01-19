from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.db.mongo import get_db
from app.models.result import (
    ResultOut,
    ResultCreate,
    MatchCorrectUpdate,
    FeedbackUpdate
)

router = APIRouter(prefix="/api/results", tags=["results"])


# Create new result
@router.post("/", response_model=ResultOut)
async def create_result(result: ResultCreate):
    db = get_db()
    collection = db["results"]
    
    # Check if result already exists for this person
    existing = await collection.find_one(
        {"personId": result.personId},
        projection={"_id": 0}
    )
    
    if existing:
        # Update existing result
        await collection.update_one(
            {"personId": result.personId},
            {
                "$set": {
                    "matchCorrect": result.matchCorrect,
                    "updatedAt": datetime.now()
                }
            }
        )
        updated = await collection.find_one(
            {"personId": result.personId},
            projection={"_id": 0}
        )
        return ResultOut(**updated)
    
    # Create new result
    result_data = result.model_dump()
    result_data["resultId"] = str(uuid.uuid4())
    result_data["createdAt"] = datetime.now()
    result_data["feedback"] = None
    result_data["updatedAt"] = None
    
    await collection.insert_one(result_data)
    
    return ResultOut(**result_data)


# Get result by personId
@router.get("/by-person/{person_id}", response_model=ResultOut)
async def get_result_by_person(person_id: str):
    db = get_db()
    collection = db["results"]
    
    doc = await collection.find_one(
        {"personId": person_id},
        projection={"_id": 0}
    )
    
    if doc is None:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return ResultOut(**doc)


# Get results by personName
@router.get("/by-name/{person_name}", response_model=List[ResultOut])
async def get_results_by_name(person_name: str):
    db = get_db()
    collection = db["results"]
    
    cursor = collection.find(
        {"personName": person_name},
        projection={"_id": 0}
    )
    results = await cursor.to_list(length=100)
    
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this name")
    
    return results


# Update matchCorrect by personId
@router.patch("/by-person/{person_id}/match", response_model=ResultOut)
async def update_match_correct(person_id: str, data: MatchCorrectUpdate):
    db = get_db()
    collection = db["results"]
    
    result = await collection.find_one({"personId": person_id})
    
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    
    await collection.update_one(
        {"personId": person_id},
        {
            "$set": {
                "matchCorrect": data.matchCorrect,
                "updatedAt": datetime.now()
            }
        }
    )
    
    updated = await collection.find_one(
        {"personId": person_id},
        projection={"_id": 0}
    )
    
    return ResultOut(**updated)


# Update feedback by personId
@router.patch("/by-person/{person_id}/feedback", response_model=ResultOut)
async def update_feedback(person_id: str, data: FeedbackUpdate):
    db = get_db()
    collection = db["results"]
    
    result = await collection.find_one({"personId": person_id})
    
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    
    await collection.update_one(
        {"personId": person_id},
        {
            "$set": {
                "feedback": data.feedback,
                "updatedAt": datetime.now()
            }
        }
    )
    
    updated = await collection.find_one(
        {"personId": person_id},
        projection={"_id": 0}
    )
    
    return ResultOut(**updated)