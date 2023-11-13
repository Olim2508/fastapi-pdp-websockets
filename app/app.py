from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from db_conf import db_session
# from db.db_conf import db_session
from api.api_v1.api import api_router

# db = db_session.session_factory()


app = FastAPI(
    title='Blog App',
    docs_url='/docs/',
    openapi_url='/docs/openapi.json',
    servers=[
        {
            "url": "http://127.0.0.1:8007",
            "description": "Local environment",
        },
        {
            "url": "https://fastapi-backend.olim.space",
            "description": "PROD environment",
        },
    ],
)

app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000/",
        "http://localhost:3000",
        "http://localhost:4000/",
        "https://blog.olim.space/",
        "https://blog.olim.space",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
