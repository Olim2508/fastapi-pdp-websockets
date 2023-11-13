from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config

DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    db=config.POSTGRES_DB,
)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
