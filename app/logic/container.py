from dishka import Provider, Scope, provide, make_container

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.memory import MemoryChatRepository
from app.settings.config import Settings
from app.logic.mediator import Mediator


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class RepositoriesProvider(Provider):
    @provide(scope=Scope.APP)
    def get_chats_mongodb_repository(self):
        ...

    @provide(scope=Scope.APP)
    def get_messages_mongodb_repository(self):
        ...

    @provide(scope=Scope.APP)
    def get_memory_chat_repository(self) -> BaseChatsRepository:
        return MemoryChatRepository()



class ConnectionsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_mongodb_connection(self):
        ...


class QueriesProvider(Provider):
    @provide
    def get_chat_detail(self):
        ...


class MediatorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_mediator(self) -> Mediator:
        return Mediator()


container = make_container(
    SettingsProvider(),
    RepositoriesProvider(),
    QueriesProvider(),
    ConnectionsProvider(),
    MediatorProvider(),
)
