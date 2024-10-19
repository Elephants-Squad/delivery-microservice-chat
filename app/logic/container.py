import functools

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.memory import MemoryChatRepository

from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator

import punq


class ContainerConfig:
    def __init__(self) -> None:
        self.container = punq.Container()

    def register_services(self) -> None:
        # Регистрация сервисов и хендлеров
        self.container.register(BaseChatsRepository, MemoryChatRepository, scope=punq.Scope.singleton)
        self.container.register(CreateChatCommandHandler)

    def register_mediator(self) -> None:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [self.container.resolve(CreateChatCommandHandler)]
        )
        self.container.register(Mediator, factory=lambda: mediator)

    def build(self) -> punq.Container:
        self.register_services()
        self.register_mediator()
        return self.container


def get_container() -> punq.Container:
    return ContainerConfig().build()
