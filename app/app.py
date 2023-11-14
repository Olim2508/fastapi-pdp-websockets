from fastapi import FastAPI, WebSocket
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
