import pytest
import string
import random
from uuid import uuid4

from datetime import datetime, UTC
from app.domain.values.messages import Text, Title
from app.domain.entities.messages import Message, Chat
from app.domain.exceptions.message import ObsceneTextException, EmptyTextException, TitleTooLongException
from mimesis import Text as MimesisText

from app.domain.events.messages import NewMessageReceivedEvent


@pytest.mark.parametrize("sentence", [
    MimesisText().sentence() * i for i in range(1, 10)
])
def test_create_message(sentence):
    text = Text(sentence)
    message = Message(text=text, chat_oid=str(uuid4()))

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
    with pytest.raises(TitleTooLongException):
        Title(mimesis_object.title() * 250)


def test_new_message_events():
    text = Text('hello world')
    message = Message(text=text, chat_oid=str(uuid4()))

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
