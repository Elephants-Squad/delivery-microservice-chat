from dataclasses import dataclass
from app.domain.values.messages import Text

@dataclass(frozen=True)
class Message:
    oid: str
    text: Text