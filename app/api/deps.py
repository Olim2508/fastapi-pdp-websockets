from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import crud
import models
import schemas
from core import security
from core.config import config
from db.db_conf import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{config.API_MAIN_PREFIX}/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> models.User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# todo modify dependency so that it gets refresh token as argument and return bool
#  value whether refresh token is valid or not
# def validate_refresh_token(db: Session = Depends(get_db),
#                            refresh_token: str = Depends(reusable_oauth2)) -> models.User:
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=[security.ALGORITHM])
#         token_data = schemas.TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = crud.user.get(db, id=token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
