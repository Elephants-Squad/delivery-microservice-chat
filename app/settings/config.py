from pydantic import computed_field, MongoDsn, Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGODB",
        extra="ignore"
    )

    port: int = Field(alias="PORT")
    host: str = Field(alias="HOST")

    @computed_field
    @property
    def url(self) -> MongoDsn:
        return f"mongodb://{self.host}:{self.port}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
