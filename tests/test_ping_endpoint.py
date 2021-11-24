from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ping_success():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json()["success"] is True
