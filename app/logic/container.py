import punq
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.mongo import MongoDBChatRepository
from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator
from app.settings.config import Settings


class ContainerConfig:
    def __init__(self) -> None:
        self.container = punq.Container()
        self.container.register(Settings, instance=Settings(), scope=punq.Scope.singleton)

    def register_services(self) -> None:
        # Регистрация сервисов и хендлеров
        self.container.register(CreateChatCommandHandler)

    def register_repositories(self) -> None:
        settings: Settings = self.container.resolve(Settings)

        self.container.register(
            BaseChatsRepository,
            factory=lambda: MongoDBChatRepository(
                mongo_db_client=AsyncIOMotorClient(str(settings.database.url), serverSelectionTimeoutMS=3000),
                mongo_db_db_name=settings.database.chat_database,
                mongo_db_collection_name=settings.database.chat_collection,
            ),
            scope=punq.Scope.singleton
        )

    def register_mediator(self) -> None:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [self.container.resolve(CreateChatCommandHandler)]
        )
        self.container.register(Mediator, factory=lambda: mediator)

    def build(self) -> punq.Container:
        self.register_services()
        self.register_repositories()
        self.register_mediator()
        return self.container


def get_container() -> punq.Container:
    return ContainerConfig().build()
