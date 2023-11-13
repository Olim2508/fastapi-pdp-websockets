from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from api.deps import get_db
from app.app import app
from app.db.session import DATABASE_TEST_URL, SessionLocal
from core.config import config
from db import Base
from tests.common import authentication_token_from_email


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_TEST_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    from app.app import app

    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = SessionLocal(bind=connection)
    # db = Session(db_engine)
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(client=client, email=config.EMAIL_TEST_USER, db=db)
