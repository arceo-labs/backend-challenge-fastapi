from fastapi.testclient import TestClient


def test_create_item(client: TestClient) -> None:
    response = client.get("/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"healthy": True, "errors": []}
