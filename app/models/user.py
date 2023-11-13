from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base
from .base import CreateUpdateDate


class User(Base, CreateUpdateDate):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    posts = relationship("Post", back_populates="author")
