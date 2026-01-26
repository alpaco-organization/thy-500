from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool

from app.db.mongo import get_db
from app.models.person import PersonOut, PersonSearchOut, SearchType
from app.services.s3 import build_s3_key_from_filename, presign_get_object
from app.utils.normalize import normalize_name
from app.routers.search_history import log_search

router = APIRouter(prefix="/api", tags=["person"])


async def _find_person(search_type: SearchType, query: str) -> PersonOut:
    q = query.strip()
    db = get_db()
    collection = db["persons"]

    if search_type == "identity":
        doc = await collection.find_one(
            {"personId": q},
            projection={
                "_id": 0,
                "personId": 1,
                "name": 1,
                "x": 1,
                "y": 1,
                "z": 1,
            },
        )
    else:
        normalized = normalize_name(q)
        # Preferred path: fast exact match against precomputed normalized field
        doc = await collection.find_one(
            {"name_normalized": normalized},
            projection={
                "_id": 0,
                "personId": 1,
                "name": 1,
                "x": 1,
                "y": 1,
                "z": 1,
            },
        )

        # Fallback (for older records not backfilled yet): diacritic-insensitive equality via collation
        if doc is None:
            doc = await collection.find_one(
                {"name": q},
                projection={
                    "_id": 0,
                    "personId": 1,
                    "name": 1,
                    "grid_filename": 1,
                    "row": 1,
                    "column": 1,
                    "x": 1,
                    "y": 1,
                },
                collation={"locale": "tr", "strength": 1},
            )
    if doc is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return PersonOut(**doc)


async def _presigned_url_for_grid_filename(grid_filename: str | None) -> str:
    if not grid_filename:
        raise HTTPException(status_code=500, detail="Missing grid filename")

    try:
        key = build_s3_key_from_filename(grid_filename)
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid grid filename")

    try:
        presigned = await run_in_threadpool(presign_get_object, key)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return presigned.url


@router.get("/search", response_model=PersonSearchOut, response_model_exclude_unset=True)
async def search_person(
    searchType: SearchType = Query(..., description='"identity" or "fullName"'),
    query: str = Query(..., min_length=1),
) -> PersonSearchOut:
    try:
        person = await _find_person(searchType, query)
        # Log successful search
        await log_search(
            search_type=searchType,
            query=query,
            person_id=person.personId,
            person_name=person.name,
            found=True,
        )
        return PersonSearchOut(
            personId=person.personId,
            name=person.name,
            x=person.x,
            y=person.y,
            z=person.z,
        )
    except HTTPException as e:
        # Log failed search (person not found)
        if e.status_code == 404:
            await log_search(
                search_type=searchType,
                query=query,
                found=False,
            )
        raise
