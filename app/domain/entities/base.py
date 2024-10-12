from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime, UTC
from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.events.base import BaseEvent


@dataclass(frozen=True)
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True
    )

    _events: list["BaseEvent"] = field(default_factory=list, kw_only=True)

    def __eq__(self, other: "BaseEntity") -> bool:
        if not isinstance(other, BaseEntity):
            raise NotImplementedError
        return self.oid == other.oid

    def __hash__(self) -> int:
        return hash(self.oid)

    def register_event(self, event: "BaseEvent") -> None:
        self._events.append(event)

    def pull_events(self) -> "list[BaseEvent]":
        registered_events = copy(self._events)
        self._events.clear()
        return registered_events
