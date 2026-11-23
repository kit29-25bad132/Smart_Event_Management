from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_validation_errors_use_standard_envelope():
    response = client.post("/api/auth/register", json={"email": "not-an-email", "password": "x"})
    assert response.status_code == 422
    assert set(response.json()["error"]) == {"code", "message", "request_id", "details"}

def test_missing_token_uses_standard_envelope():
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "HTTP_401"
