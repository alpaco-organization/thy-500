from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.db.mongo import get_db, mongo
from app.routers.person import router as person_router
from app.routers.result import router as result_router
from app.routers.search_history import router as search_history_router
from app.routers import auth

app = FastAPI(title="thy-500-backend")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert validation errors to string detail format."""
    errors = exc.errors()
    if errors:
        # Get first error message
        first_error = errors[0]
        field = first_error.get("loc", ["", ""])[-1]
        msg = first_error.get("msg", "Validation error")
        detail = f"{field}: {msg}" if field else msg
    else:
        detail = "Validation error"

    return JSONResponse(
        status_code=422,
        content={"detail": detail}
    )

# allow_origins = ["*"] if settings.cors_allow_origins.strip() == "*" else [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]
allow_origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def health():
    return {"ok": True}


app.include_router(person_router)
app.include_router(result_router)
app.include_router(search_history_router)
app.include_router(auth.router)

@app.on_event("startup")
async def _startup():
    db = get_db()
    await db["persons"].create_index("name_normalized")
    await db["results"].create_index("personName")
    await db["search_history"].create_index("createdAt")
    await db["search_history"].create_index("query")

@app.on_event("shutdown")
async def _shutdown():
    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None
