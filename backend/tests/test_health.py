from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ready() -> None:
    response = client.get("/api/ready")
    assert response.status_code in (200, 503)
    if response.status_code == 200:
        assert response.json()["status"] == "ready"
    else:
        assert response.json()["error"]["message"] == "Database is unavailable"
        assert response.json()["error"]["code"] == "HTTP_503"

