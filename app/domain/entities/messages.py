__all__ = ["Message", "Chat"]

from dataclasses import dataclass, field
from typing import Set

from app.domain.events.messages import NewMessageReceivedEvent, NewChatCreatedEvent
from app.domain.values.messages import Text, Title
from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text
    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__


@dataclass(eq=False)
class ChatListener(BaseEntity):
    ...


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: Set[Message] = field(
        default_factory=set,
        kw_only=True
    )
    listeners: set[ChatListener] = field(default_factory=set, kw_only=True)
    is_deleted: bool = field(default=False, kw_only=True)

    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreatedEvent(
            chat_oid=new_chat.oid,
            chat_title=new_chat.title.as_generic_type())
        )
        return new_chat

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(),
            chat_oid=self.oid,
            message_oid=message.oid,
        ))
