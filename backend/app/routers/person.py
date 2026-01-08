import re

from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool

from app.db.mongo import get_db
from app.models.person import PersonOut, PersonSearchOut, SearchType
from app.services.s3 import build_s3_key_from_xy, presign_get_object

router = APIRouter(prefix="/api", tags=["person"])


async def _find_person(search_type: SearchType, query: str) -> PersonOut:
    q = query.strip()
    db = get_db()
    collection = db["persons"]

    if search_type == "identity":
        mongo_query = {"personId": q}
    else:
        escaped = re.escape(q)
        mongo_query = {"name": {"$regex": f"^{escaped}$", "$options": "i"}}

    doc = await collection.find_one(
        mongo_query,
        projection={"_id": 0, "personId": 1, "name": 1, "x": 1, "y": 1},
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return PersonOut(**doc)


async def _presigned_url_for_xy(x: float, y: float) -> str:
    # S3 key format expects integer coordinates (grid_x{X}_y{Y}.png)
    try:
        xi = int(x)
        yi = int(y)
    except (TypeError, ValueError):
        raise HTTPException(status_code=500, detail="Invalid person coordinates")

    try:
        key = build_s3_key_from_xy(str(xi), str(yi))
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid person coordinates")

    try:
        presigned = await run_in_threadpool(presign_get_object, key)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return presigned.url


@router.get("/search", response_model=PersonSearchOut)
async def search_person(
    searchType: SearchType = Query(..., description='"identity" or "fullName"'),
    query: str = Query(..., min_length=1),
) -> PersonSearchOut:
    person = await _find_person(searchType, query)
    url = await _presigned_url_for_xy(person.x, person.y)
    return PersonSearchOut(name=person.name, x=person.x, y=person.y, url=url)
