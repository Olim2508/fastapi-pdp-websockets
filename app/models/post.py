from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base
from .base import CreateUpdateDate

if TYPE_CHECKING:
    from .category import Category  # noqa: F401
    from .user import User  # noqa: F401


class Post(Base, CreateUpdateDate):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts")
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    category = relationship("Category", back_populates="posts")
