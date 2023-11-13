from typing import TypeVar, List

from pydantic import BaseModel

from db import Base

ModelType = TypeVar("ModelType", bound=Base)


class ModelResponseList(BaseModel):
    count: int
    result: List[ModelType]
