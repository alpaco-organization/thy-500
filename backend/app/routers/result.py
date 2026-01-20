from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.db.mongo import get_db
from app.models.result import ResultOut, ResultCreate

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/", response_model=ResultOut)
async def create_result(result: ResultCreate):
    db = get_db()
    results_collection = db["results"]
    persons_collection = db["persons"]
    if result.matchCorrect is not None and result.feedback is not None:
        raise HTTPException(
            status_code=400,
            detail="Cannot send both matchCorrect and feedback. Only one is allowed per request."
        )
    if result.matchCorrect is None and result.feedback is None:
        raise HTTPException(
            status_code=400,
            detail="Either matchCorrect or feedback must be provided"
        )
    # Base result data
    result_data = {
        "resultId": str(uuid.uuid4()),
        "personId": result.personId,
        "personName": result.personName,
        "createdAt": datetime.now()
    }
    
    # Optional fields - only include if not None
    optional_fields = {
        k: v for k, v in {
            "matchCorrect": result.matchCorrect,
            "feedback": result.feedback
        }.items() if v is not None
    }
    
    result_data.update(optional_fields)
    await results_collection.insert_one(result_data)
    
    # Update persons only with provided fields
    if optional_fields:
        await persons_collection.update_one(
            {"personId": result.personId},
            {"$set": optional_fields}
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