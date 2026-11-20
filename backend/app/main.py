import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper(), format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["GET"], allow_headers=["*"])

@app.get("/api/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"application": settings.app_name, "status": "healthy"}

@app.get("/api/ready", tags=["system"])
async def ready() -> dict[str, str]:
    return {"application": settings.app_name, "status": "ready"}

