from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from typing import Optional

from app.db.mongo import get_db
from app.models.person import PersonOut, PersonSearchOut, SearchType
from app.services.s3 import build_s3_key_from_filename, presign_get_object
from app.utils.normalize import normalize_name
from app.routers.search_history import log_search

router = APIRouter(prefix="/api", tags=["person"])

# Error messages by language
ERROR_MESSAGES = {
    "tr": {
        "person_not_found": "Kişi bulunamadı",
        "missing_grid_filename": "Grid dosya adı eksik",
        "invalid_grid_filename": "Geçersiz grid dosya adı",
    },
    "en": {
        "person_not_found": "Person not found",
        "missing_grid_filename": "Missing grid filename",
        "invalid_grid_filename": "Invalid grid filename",
    }
}


def get_lang(accept_language: Optional[str]) -> str:
    """Get language from Accept-Language header."""
    if accept_language and "tr" in accept_language.lower():
        return "tr"
    return "en"


def get_error_message(key: str, lang: str) -> str:
    """Get error message by key and language."""
    return ERROR_MESSAGES.get(lang, ERROR_MESSAGES["en"]).get(key, key)


async def _find_person(search_type: SearchType, query: str, lang: str = "en") -> PersonOut:
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
        raise HTTPException(
            status_code=404,
            detail=get_error_message("person_not_found", lang)
        )

    return PersonOut(**doc)


async def _presigned_url_for_grid_filename(grid_filename: str | None, lang: str = "en") -> str:
    if not grid_filename:
        raise HTTPException(
            status_code=500,
            detail=get_error_message("missing_grid_filename", lang)
        )

    try:
        key = build_s3_key_from_filename(grid_filename)
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail=get_error_message("invalid_grid_filename", lang)
        )

    try:
        presigned = await run_in_threadpool(presign_get_object, key)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return presigned.url


@router.get("/search", response_model=PersonSearchOut, response_model_exclude_unset=True)
async def search_person(
    searchType: SearchType = Query(..., description='"identity" or "fullName"'),
    query: str = Query(..., min_length=1),
    accept_language: Optional[str] = Header(None, alias="Accept-Language"),
) -> PersonSearchOut:
    lang = get_lang(accept_language)
    try:
        person = await _find_person(searchType, query, lang)
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
