import pytest
import string
import random

from datetime import datetime, UTC
from app.domain.values.messages import Text, Title
from app.domain.entities.messages import Message, Chat
from app.domain.exceptions import ObsceneTextException, EmptyTextException, TextTooLongException
from mimesis import Text as MimesisText


@pytest.fixture(scope='module')
def mimesis_object():
    return MimesisText()


@pytest.mark.parametrize("sentence", [
    MimesisText().sentence() * i for i in range(1, 10)
])
def test_create_message(sentence):
    text = Text(sentence)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.now(UTC).date()


def test_empty_message():
    with pytest.raises(EmptyTextException):
        Text("")


@pytest.mark.parametrize('obscene_text', [
    "хуй",
    "блять",
    "пизда",
    "пиздец",
    "хуйня"
])
def test_create_obscene_text(obscene_text):
    with pytest.raises(ObsceneTextException):
        Text(obscene_text)

@pytest.mark.parametrize("name", [
    ''.join(random.choices(string.ascii_letters, k=random.randint(5, 25)))
])
def test_create_chat_success(name):
    title = Title(name)
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.now(UTC).date()


def test_create_chat_failure(mimesis_object):
    with pytest.raises(TextTooLongException):
        Title(mimesis_object.title() * 250)
