from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenAll(Token):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
