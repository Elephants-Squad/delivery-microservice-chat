from dataclasses import dataclass
from app.logic.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_oid: str
    message_text: str
    chat_oid: str


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: str
    title: str
