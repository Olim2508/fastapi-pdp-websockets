import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import crud
import models
import schemas
from core.config import config
from models import User


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_test_category(db: Session) -> models.Category:
    category_in = schemas.CategoryCreate(title="sport")
    return crud.category.create(db, obj_in=category_in)


def create_test_categories(db: Session):
    for i in range(3):
        category_in = schemas.CategoryCreate(title=f"category {i}")
        crud.category.create(db, obj_in=category_in)


def create_test_posts(db: Session, author=None):
    category = create_test_category(db)
    if not author:
        author = create_test_user(db)
    for i in range(3):
        post_in = schemas.PostCreate(
            title=f"How to be a Pirate series {i}",
            content="Lorem ipsum dolor sit",
        )
        crud.post.create_(db, obj_in=post_in, category=category, author_id=author.id)


def create_test_post(db: Session):
    category = create_test_category(db)
    author = create_test_user(db)
    post_in = schemas.PostCreate(
        title="Awesome post",
        content="Lorem ipsum dolor sit",
    )
    return crud.post.create_(db, obj_in=post_in, category=category, author_id=author.id)


def create_test_user(db: Session):
    user_in = schemas.UserCreate(email="mail@test.com", password="123456")
    return crud.user.create(db, obj_in=user_in)


def user_authentication_headers(*, client: TestClient, email: str, password: str) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{config.API_MAIN_PREFIX}/login/", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(*, client: TestClient, email: str, db: Session) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = schemas.UserCreate(email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = schemas.UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
