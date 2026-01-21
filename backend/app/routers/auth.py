from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_admin
from app.core.security import verify_password, create_access_token
from app.db.mongo import get_db
from app.models.user import LoginRequest, Token, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest):
    db = get_db()

    user = await db.users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
        )

    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )

    return Token(access_token=access_token)


@router.get("/verify", response_model=UserOut)
async def verify(admin: dict = Depends(get_current_admin)):
    db = get_db()

    user = await db.users.find_one({"email": admin["sub"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserOut(
        userId=str(user["_id"]),
        email=user["email"],
        role=user["role"],
        is_active=user["is_active"],
        created_at=user["created_at"],
    )
