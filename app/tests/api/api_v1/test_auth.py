from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import config
from tests.common import create_test_user


def test_register_user(client: TestClient, db: Session) -> None:
    data = {"email": "wrongmail", "password": "123456"}
    response = client.post(
        f"{config.API_MAIN_PREFIX}/user/register",
        json=data,
    )
    assert response.status_code == 422

    data['email'] = "mail@test.com"
    response = client.post(
        f"{config.API_MAIN_PREFIX}/user/register",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert "id" in content


def test_login(client: TestClient, db: Session) -> None:
    user = create_test_user(db)
    login_data = {
        "username": user.email,
        "password": "123456",
    }
    r = client.post(f"{config.API_MAIN_PREFIX}/login/", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_get_user_me(client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]) -> None:
    r = client.get(f"{config.API_MAIN_PREFIX}/user/me", headers=normal_user_token_headers)
    assert r.status_code == 200
    current_user = r.json()
    assert current_user['email'] == "test@gmail.com"
    assert current_user['is_active']
