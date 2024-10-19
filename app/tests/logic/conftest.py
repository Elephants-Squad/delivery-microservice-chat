from punq import (
    Container,
    Scope,
)
from pytest import fixture
from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.memory import MemoryChatRepository
from app.logic.mediator import Mediator
from app.logic.container import get_container
from mimesis import Text

@fixture(scope='module')
def mimesis_object():
    return Text()


@fixture(scope='function')
def container() -> Container:
    container = get_container()
    container.register(BaseChatsRepository, MemoryChatRepository, scope=Scope.singleton)

    return container


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
