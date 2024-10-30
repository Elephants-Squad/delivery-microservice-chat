from pydantic import computed_field, MongoDsn, Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGO_DB",
        extra="ignore"
    )

    url: MongoDsn = Field(alias="MONGO_DB_URL")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
