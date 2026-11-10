"""Tests for the health-check and database-health endpoints."""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """GET /health should return a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "servicefind-api"


def test_root() -> None:
    """GET / should return a welcome payload."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


def test_database_health_connected() -> None:
    """GET /health/database should report healthy when ping succeeds."""
    with patch("app.database.ping_database", new=AsyncMock(return_value=True)):
        response = client.get("/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"]["connected"] is True


def test_database_health_disconnected() -> None:
    """GET /health/database should report unhealthy when ping fails."""
    with patch("app.database.ping_database", new=AsyncMock(return_value=False)):
        response = client.get("/health/database")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["database"]["connected"] is False
