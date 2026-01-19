from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.mongo import get_db, mongo
from app.routers.person import router as person_router
from app.routers.result import router as result_router

app = FastAPI(title="thy-500-backend")

allow_origins = ["*"] if settings.cors_allow_origins.strip() == "*" else [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]

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


@app.on_event("startup")
async def _startup():
    db = get_db()
    await db["persons"].create_index("name_normalized")
    await db["results"].create_index("personName")

@app.on_event("shutdown")
async def _shutdown():
    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None
