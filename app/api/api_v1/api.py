from fastapi import APIRouter

from api.api_v1.endpoints import categories, login, posts, users
from core.config import config

api_router = APIRouter(prefix=config.API_MAIN_PREFIX)

api_router.include_router(login.router, tags=["login"])
api_router.include_router(posts.router, prefix='/post', tags=['Post'])
api_router.include_router(categories.router, prefix='/category', tags=['Category'])
api_router.include_router(users.router, prefix='/user', tags=['User'])
