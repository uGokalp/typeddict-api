from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

str_example = '{"a": "a"}'


def test_basic_successful():
    response = client.post(
        "/dict",
        json={"code": str_example},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200


def test_basic_unsuccessful():
    response = client.post(
        "/dict",
        json={"code": "abc"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422
