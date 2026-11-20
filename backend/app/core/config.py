from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Agentic AI Smart Event Management System API"
    environment: str = "development"
    log_level: str = "INFO"
    backend_cors_origins: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

