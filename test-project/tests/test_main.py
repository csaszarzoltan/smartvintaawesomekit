"""Sample tests for test-project."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
