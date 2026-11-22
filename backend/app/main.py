import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from sqlalchemy import text
from fastapi import Request
from fastapi.responses import JSONResponse
from app.db.session import engine
from app.api import auth, users, venues, events, registrations

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper(), format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)

app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router); app.include_router(users.router); app.include_router(venues.router); app.include_router(events.router); app.include_router(registrations.router)

@app.exception_handler(Exception)
async def unhandled(_: Request, exc: Exception):
    logger.exception("Unhandled application error")
    return JSONResponse(status_code=500, content={"error": {"code": "INTERNAL_ERROR", "message": "An internal error occurred"}})

@app.get("/api/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"application": settings.app_name, "status": "healthy"}

@app.get("/api/ready", tags=["system"])
async def ready() -> dict[str, str]:
    try:
        with engine.connect() as connection: connection.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning("Readiness database check failed: %s", type(exc).__name__)
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc
    return {"application": settings.app_name, "status": "ready"}

