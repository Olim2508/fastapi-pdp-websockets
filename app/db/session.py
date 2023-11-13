import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from core.config import config

# todo by file this is not used. Need to migrate db_conf.py content file here

DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    db=config.POSTGRES_DB,
)

DATABASE_TEST_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    db=config.POSTGRES_DB + '_test',
)


def validate_db():
    engine = create_engine(
        DATABASE_URL, pool_size=config.POSTGRES_POOL_SIZE, max_overflow=config.POSTGRES_POOL_OVERFLOW
    )
    if not database_exists(engine.url):
        create_database(engine.url)
        logging.info("New Database Created" + str(database_exists(engine.url)))
    else:
        logging.info("Database Already Exists")

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = validate_db()
