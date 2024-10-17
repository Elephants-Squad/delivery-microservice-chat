from fastapi import FastAPI
from app.logic.container import container

from app.application.api.messages.handlers import router as messages_router

app = FastAPI(
    title="Microservice for messages",
    docs_url="/api/docs",
    description="A simple microservice written with DDD pattern for messaging with users",
    debug=True,
)

app.include_router(messages_router)
