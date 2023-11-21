from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api import deps
from api.api_v1.api import api_router
from sqlalchemy.orm import Session

# db = db_session.session_factory()
from api.deps import get_current_user
from utils import SocketManager

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
async def websocket_endpoint(websocket: WebSocket,
                             db: Session = Depends(deps.get_db),
                             token: str = None,
                             ):
    if token is None:
        await websocket.close(code=1008)
    user = None
    try:
        user = deps.get_current_user(db, token)
    except HTTPException:
        await websocket.close(code=1008)
    manager = SocketManager()

    await manager.connect(websocket, user.full_name)
    response = {
        "sender": user.full_name,
        "message": "got connected"
    }
    await manager.broadcast(response)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.full_name)
        response['message'] = "left"
        await manager.broadcast(response)
