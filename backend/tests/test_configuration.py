import pytest
from pydantic import ValidationError
from app.core.config import Settings

def test_jwt_secret_rejects_missing_or_placeholder():
    with pytest.raises(ValidationError): Settings(jwt_secret_key="")
    with pytest.raises(ValidationError): Settings(jwt_secret_key="development-only-change-me")
    with pytest.raises(ValidationError): Settings(jwt_secret_key="short")

def test_jwt_secret_accepts_long_random_value():
    settings = Settings(jwt_secret_key="a" * 64)
    assert len(settings.jwt_secret_key) == 64
