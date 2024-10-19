from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from app.logic.container import ContainerConfig
from app.application.api.messages.handlers import router as messages_router

app = VersionedFastAPI(
    FastAPI(
        title="Microservice for messages",
        description="A simple microservice written with DDD pattern for messaging with users",
        root_path="/api",
        version="0.1.0",
        debug=True,
    ),
    version_format='{major}',
    prefix_format='/api/v{major}'
)

container_cfg = ContainerConfig()
app.state.ioc_container = container_cfg.build()

app.include_router(messages_router)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
