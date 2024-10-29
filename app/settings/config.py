from pydantic import computed_field, MongoDsn
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGODB",
        extra="ignore"
    )

    port: int
    name: str

    @computed_field
    @property
    def url(self) -> MongoDsn:
        return f"mongodb://{self.name}:{self.port}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
