from functools import lru_cache
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Agentic AI Smart Event Management System API"
    environment: str = "development"
    log_level: str = "INFO"
    backend_cors_origins: str = "http://localhost:3000"
    database_url: str = "postgresql+psycopg://smart_event:change-me@localhost:5432/smart_event_management"
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @model_validator(mode="after")
    def validate_jwt_secret(self):
        known_placeholders = {"", "change-me", "replace-with-a-long-random-secret", "development-only-change-me"}
        if self.jwt_secret_key in known_placeholders or len(self.jwt_secret_key) < 32:
            raise ValueError("JWT_SECRET_KEY must be a non-placeholder value of at least 32 characters")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

