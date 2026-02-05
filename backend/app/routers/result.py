from fastapi import APIRouter, Header, HTTPException, Response, Query
from typing import List, Optional
import uuid
from datetime import datetime

from app.db.mongo import get_db
from app.models.result import ResultOut, ResultCreate
from app.utils.normalize import normalize_name

router = APIRouter(prefix="/api/results", tags=["results"])

# Error messages by language
ERROR_MESSAGES = {
    "tr": {
        "feedback_required": "Geri bildirim sağlanmalıdır",
        "no_results_found": "Sonuç bulunamadı",
    },
    "en": {
        "feedback_required": "Feedback must be provided",
        "no_results_found": "No results found",
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


@router.post("/")
async def create_result(
    result: ResultCreate,
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    lang = get_lang(accept_language)
    db = get_db()
    results_collection = db["results"]
    persons_collection = db["persons"]

    if result.feedback is None:
        raise HTTPException(
            status_code=400,
            detail=get_error_message("feedback_required", lang)
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
        query = {
            "$or": [
                {"personId": {"$regex": search, "$options": "i"}},
                {"personName": {"$regex": search, "$options": "i"}}
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
async def get_results_by_person(
    person_id: str,
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    lang = get_lang(accept_language)
    db = get_db()
    collection = db["results"]

    cursor = collection.find(
        {"personId": person_id},
        projection={"_id": 0}
    )
    results = await cursor.to_list(length=100)

    if not results:
        raise HTTPException(
            status_code=404,
            detail=get_error_message("no_results_found", lang)
        )

    return results