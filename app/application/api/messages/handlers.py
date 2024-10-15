from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from app.application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.logic.mediator import Mediator

from app.logic.commands.messages import CreateChatCommand

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post(
    "/",
)
@inject
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        mediator: FromDishka[Mediator]
) -> CreateChatResponseSchema:

    await mediator.handle_command(CreateChatCommand(title=schema.title))

