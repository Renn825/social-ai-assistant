from fastapi.testclient import TestClient

from app.main import app


def test_health_does_not_require_api_key():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200


def test_protected_route_requires_api_key():
    with TestClient(app) as client:
        response = client.get("/api/v1/posts")
        assert response.status_code == 401


def test_protected_route_accepts_valid_api_key():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/posts",
            headers={"X-API-Key": "test-api-key"},
        )
        assert response.status_code == 200
