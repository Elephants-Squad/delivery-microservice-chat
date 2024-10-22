from pytest import fixture
from punq import Container, Scope
from app.logic.container import get_container
from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.memory import MemoryChatRepository


@fixture(scope='function')
def container() -> Container:
    container = get_container()
    container.register(BaseChatsRepository, MemoryChatRepository, scope=Scope.singleton)

    return container
