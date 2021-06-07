from typing import Dict

from faker.proxy import Faker
from fastapi.testclient import TestClient


def test_read_users(client: TestClient, superuser_token_headers: Dict[str, str]):
    r = client.get("/user/", headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert isinstance(result, list)
    assert len(result) > 0


def test_read_users_normal_user_only_includes_self(
    client: TestClient, normal_user_token_headers: Dict[str, str]
):
    normal_user = client.get(
        "/login/test-token", headers=normal_user_token_headers
    ).json()
    r = client.get("/user/", headers=normal_user_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert result == [normal_user]


def test_create_user(
    client: TestClient, superuser_token_headers: Dict[str, str], faker: Faker
):
    user_in = {
        "email": faker.email(),
        "password": faker.password(),
    }
    r = client.post("/user/", headers=superuser_token_headers, json=user_in)
    result = r.json()
    assert r.status_code == 201
    assert result["id"] is not None
    assert result["email"] == user_in["email"]
    assert result["is_active"] is True
    assert result["is_superuser"] is False
    assert "password" not in result


def test_create_user_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str], faker: Faker
):
    user_in = {
        "email": faker.email(),
        "password": faker.password(),
    }
    r = client.post("/user/", headers=normal_user_token_headers, json=user_in)
    result = r.json()
    assert r.status_code == 403
    assert result["detail"] == "The user doesn't have enough privileges"


def test_get_user_normal_user_forbidden_for_other_user(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    normal_user_token_headers: Dict[str, str],
    faker: Faker,
):
    other_user = client.post(
        "/user/",
        headers=superuser_token_headers,
        json={"email": faker.email(), "password": faker.password()},
    ).json()

    r = client.get(f"/user/{other_user['id']}", headers=normal_user_token_headers)
    result = r.json()
    assert r.status_code == 403
    assert result["detail"] == "The user doesn't have enough privileges"
