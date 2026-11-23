import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from sqlalchemy import text
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
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

def _error(code: str, message: str, request: Request, details=None):
    return {"error": {"code": code, "message": message, "request_id": request.headers.get("X-Request-ID", "unassigned"), "details": details or {}}}

@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, headers=exc.headers, content=_error(f"HTTP_{exc.status_code}", str(exc.detail), request))

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=_error("VALIDATION_ERROR", "Request validation failed", request, exc.errors()))

@app.exception_handler(IntegrityError)
async def integrity_error(request: Request, _: IntegrityError):
    return JSONResponse(status_code=409, content=_error("INTEGRITY_CONFLICT", "The requested change conflicts with existing data", request))

@app.get("/api/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"application": settings.app_name, "status": "healthy"}

@app.get("/api/ready", tags=["system"])
async def ready() -> dict[str, str]:
    try:
        with engine.connect() as connection: connection.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning("Readiness database check failed: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc
    return {"application": settings.app_name, "status": "ready"}

