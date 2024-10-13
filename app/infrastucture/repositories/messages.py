from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseChatRepository(ABC):

    @abstractmethod
    def check_chat_exists_by_title(self, title: str) -> bool:
        ...
