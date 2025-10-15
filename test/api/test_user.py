from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.api.user import get_user_service
from app.db.schema import Base
from app.services.user_service import UserService
from app.main import app
from test.test_db import TestingSessionLocal, engine


@pytest.fixture(scope="function")
def client() -> Iterator[TestClient]:
    def override_get_user_service() -> Iterator[UserService]:
        session = TestingSessionLocal()
        try:
            yield UserService(session=session)
        finally:
            session.close()

    app.dependency_overrides[get_user_service] = override_get_user_service

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client


def test_create_user_returns_created_user(client: TestClient) -> None:
    payload = {"name": "test-user", "password": "secret"}

    response = client.post("/users", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["password"] == payload["password"]
    assert data["id"] > 0


def test_get_user_returns_user(client: TestClient) -> None:
    create_response = client.post(
        "/users", json={"name": "lookup", "password": "pw"}
    )
    created = create_response.json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_user_missing_returns_404(client: TestClient) -> None:
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_replaces_data(client: TestClient) -> None:
    create_response = client.post(
        "/users", json={"name": "before", "password": "pw"}
    )
    created = create_response.json()

    update_payload = {"name": "after", "password": "newpw"}
    response = client.put(f"/users/{created['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["name"] == update_payload["name"]
    assert data["password"] == update_payload["password"]


def test_update_user_missing_returns_404(client: TestClient) -> None:
    response = client.put(
        "/users/999", json={"name": "who", "password": "cares"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_returns_success(client: TestClient) -> None:
    create_response = client.post(
        "/users", json={"name": "deleteme", "password": "pw"}
    )
    created = create_response.json()

    response = client.delete(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == {"success": True}

    list_response = client.get("/users")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_delete_user_missing_returns_404(client: TestClient) -> None:
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
