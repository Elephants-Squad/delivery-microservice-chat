from dataclasses import (
    dataclass,
    field,
)
from copy import copy
from typing import Iterable
from app.domain.entities.messages import Chat, ChatListener
from app.infrastucture.repositories.messages.base import BaseChatsRepository


@dataclass
class MemoryChatRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(
                chat for chat in self._saved_chats if chat.oid == oid
            )
        except StopIteration:
            return None

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat for chat in self._saved_chats if chat.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def get_all_chats(self, limit: int, offset: int) -> Iterable[Chat]:
        return self._saved_chats[offset:offset + limit]

    async def delete_chat_by_oid(self, chat_oid: str) -> None:
        if not self._saved_chats:
            raise ValueError("Чатов нет")

        for chat in copy(self._saved_chats):
            if chat.oid == chat_oid:
                self._saved_chats.remove(chat)

    async def add_telegram_listener(self, chat_oid: str, telegram_chat_id: str):
        ...

    async def get_all_chat_listeners(self, chat_oid: str) -> Iterable[ChatListener]:
        ...
