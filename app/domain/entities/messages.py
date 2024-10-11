__all__ = ["Message", "Chat"]

from dataclasses import dataclass, field
from typing import Set

from app.domain.values.messages import Text, Title
from app.domain.entities.base import BaseEntity


@dataclass(frozen=True)
class Message(BaseEntity):
    text: Text


@dataclass(frozen=True)
class Chat(BaseEntity):
    title: Title
    messages: Set[Message] = field(
        default_factory=set,
        kw_only=True
    )