from pydantic import computed_field, MongoDsn, Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGO_DB",
        extra="ignore"
    )

    port: int = Field(alias="MONGO_DB_PORT")
    host: str = Field(alias="MONGO_DB_HOST")
    chat_database: str = Field(default="chat", alias="MONGO_DB_CHAT_DATABASE")
    chat_collection: str = Field(default="chat", alias="MONGO_DB_CHAT_COLLECTION")

    @computed_field
    @property
    def url(self) -> MongoDsn:
        return f"mongodb://{self.host}:{self.port}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
