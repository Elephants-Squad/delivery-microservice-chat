__all__ = ["Message", "Chat"]

from dataclasses import dataclass, field
from typing import Set

from app.domain.values.messages import Text, Title
from app.domain.entities.base import BaseEntity


@dataclass(frozen=True)
class Message(BaseEntity):
    text: Text
    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__


@dataclass(frozen=True)
class Chat(BaseEntity):
    title: Title
    messages: Set[Message] = field(
        default_factory=set,
        kw_only=True
    )
    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
