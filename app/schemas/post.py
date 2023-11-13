from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Shared properties
from schemas import Category

# todo fix circular import and import user like "from schemas import User" this
from .user import User


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# Properties to receive on post creation
class PostCreate(PostBase):
    title: str
    content: str
    category: Category | int = None


class PostCreateDB(PostBase):
    title: str
    content: str
    category: Category | int


# Properties to receive on item update
class PostUpdate(PostBase):
    category: int


# Properties shared by models stored in DB
class PostInDBBase(PostBase):
    id: int
    title: str
    # author: str
    content: str

    class Config:
        orm_mode = True


# Properties to return to client
class Post(PostInDBBase):
    category: Category | None = None
    author: User | None = None


# Properties stored in DB
class PostInDB(PostInDBBase):
    pass
