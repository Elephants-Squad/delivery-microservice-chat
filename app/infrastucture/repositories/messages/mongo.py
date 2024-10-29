from dataclasses import dataclass

from app.infrastucture.repositories.messages.base import BaseChatsRepository
from motor.core import AgnosticClient


@dataclass
class MongoDBChatRepository(BaseChatsRepository):
    mongo_db_client: AgnosticClient
    mongo_db_name: str
    mongo_collection_name: str

    