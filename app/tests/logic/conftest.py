from mimesis import Text
from punq import Container
from pytest import fixture

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.logic.mediator import Mediator
from app.tests.conftest import container


@fixture(scope='module')
def mimesis_object():
    return Text()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
