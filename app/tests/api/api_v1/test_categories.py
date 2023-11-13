from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import config
from tests.common import create_test_categories, create_test_category


def test_create_category(client: TestClient, db: Session) -> None:
    data = {"title": "Foo"}
    response = client.post(
        f"{config.API_MAIN_PREFIX}/category/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert "id" in content


def test_read_categories(client: TestClient, db: Session) -> None:
    create_test_categories(db)
    response = client.get(f"{config.API_MAIN_PREFIX}/category/")
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 3


def test_get_category(client: TestClient, db: Session) -> None:
    category = create_test_category(db)
    response = client.get(f"{config.API_MAIN_PREFIX}/category/{category.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == category.title
    assert content["id"] == category.id
