from punq import Container

from functools import lru_cache

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.memory import MemoryChatRepository

from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.settings.config import Settings
from app.logic.mediator import Mediator



@lru_cache(1)
def init_container() -> Container:
    cont = Container()

    cont.register(BaseChatsRepository, MemoryChatRepository)
    cont.register(CreateChatCommandHandler)

    def create_mediator():
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [cont.resolve(CreateChatCommandHandler)]
        )

        return mediator

    cont.register(Mediator, factory=create_mediator)

    return cont


container = init_container()
