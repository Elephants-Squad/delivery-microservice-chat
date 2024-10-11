from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime, UTC


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

    def __eq__(self, other: "BaseEntity") -> bool:
        if not isinstance(other, BaseEntity):
            raise NotImplementedError
        return self.oid == other.oid

    def __hash__(self) -> int:
        return hash(self.oid)
