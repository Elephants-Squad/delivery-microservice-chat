from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from motor.core import AgnosticClient

from app.domain.entities.messages import Chat, ChatListener
from app.infrastucture.repositories.messages.base import BaseChatsRepository
from app.infrastucture.repositories.messages.converters import convert_chat_entity_to_document, \
    convert_chat_document_to_entity


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatRepository(BaseChatsRepository, BaseMongoDBRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={'title': title}))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'oid': oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))

    async def get_all_chats(self, limit: int, offset: int) -> Iterable[Chat]:
        ...

    async def delete_chat_by_oid(self, chat_oid: str) -> None:
        await self._collection.delete_one({'oid': chat_oid})

    async def add_telegram_listener(self, chat_oid: str, telegram_chat_id: str):
        ...

    async def get_all_chat_listeners(self, chat_oid: str) -> Iterable[ChatListener]:
        ...
