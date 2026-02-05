from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import Optional

from app.core.deps import get_current_admin
from app.core.security import verify_password, create_access_token
from app.db.mongo import get_db
from app.models.user import LoginRequest, Token, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Error messages by language
ERROR_MESSAGES = {
    "tr": {
        "invalid_credentials": "Geçersiz e-posta veya şifre",
        "user_not_active": "Kullanıcı aktif değil",
        "user_not_found": "Kullanıcı bulunamadı",
    },
    "en": {
        "invalid_credentials": "Invalid email or password",
        "user_not_active": "User is not active",
        "user_not_found": "User not found",
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


@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    lang = get_lang(accept_language)
    db = get_db()

    user = await db.users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_error_message("invalid_credentials", lang),
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_error_message("user_not_active", lang),
        )

    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )

    return Token(access_token=access_token)


@router.get("/verify")
async def verify(
    admin: dict = Depends(get_current_admin),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    lang = get_lang(accept_language)
    db = get_db()

    user = await db.users.find_one({"email": admin["sub"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_error_message("user_not_found", lang),
        )

    return {}
