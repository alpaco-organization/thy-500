from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime
from app.db.mongo import get_db
from app.models.result import ResultOut, ResultCreate

router = APIRouter(prefix="/api/results", tags=["results"])


# Create new result
@router.post("/", response_model=ResultOut)
async def create_result(result: ResultCreate):
    db = get_db()
    collection = db["results"]
    
    result_data = result.model_dump()
    result_data["resultId"] = str(uuid.uuid4())
    result_data["createdAt"] = datetime.now()
    
    await collection.insert_one(result_data)
    
    return ResultOut(**result_data)


# Get one result by id
@router.get("/by-id/{result_id}", response_model=ResultOut)
async def get_result(result_id: str):
    db = get_db()
    collection = db["results"]
    
    doc = await collection.find_one(
        {"resultId": result_id},
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
