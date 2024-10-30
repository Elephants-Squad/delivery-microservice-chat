from pydantic import computed_field, MongoDsn, Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGO_DB",
        extra="ignore"
    )

    url: MongoDsn = Field(alias="MONGO_DB_URL")
    chat_database: str = Field(default="chat", alias="MONGO_DB_CHAT_DATABASE")
    chat_collection: str = Field(default="chat", alias="MONGO_DB_CHAT_COLLECTION")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
