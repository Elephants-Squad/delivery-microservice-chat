from fastapi import APIRouter, HTTPException, status
from typing import Annotated

from fastapi.params import Depends

from app.application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.domain.exceptions.base import ApplicationException
from app.logic.container import get_container
from app.logic.mediator import Mediator
from app.logic.dependecies import Service
from app.logic.commands.messages import CreateChatCommand
from app.application.api.schemas import ErrorSchema

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт создаёт новый чат, если чат с таким названием существует, то возвращается 400 ошибка',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_chat_handler(chat_schema: CreateChatRequestSchema, mediator: Mediator = Service(Mediator)):
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=chat_schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})

    return CreateChatResponseSchema.from_entity(chat)
