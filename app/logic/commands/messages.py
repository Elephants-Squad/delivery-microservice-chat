from dataclasses import dataclass

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.logic.commands.base import BaseCommand, CommandHandler
from app.domain.entities.messages import Chat
from app.logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from app.domain.values.messages import Title


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatsRepository
    
    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        chat = Chat.create_chat(title)
        return chat
