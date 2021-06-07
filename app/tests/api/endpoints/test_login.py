from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    }
    r = client.post("/login/access-token", data=login_data)
    token = r.json()
    assert r.status_code == 200
    assert "access_token" in token
    assert token["access_token"]


def test_use_access_token_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        "/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_user_access_token_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
):
    r = client.get(
        "/login/test-token",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
