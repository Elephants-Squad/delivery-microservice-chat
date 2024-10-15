from dishka import Provider, Scope, provide
from app.settings.config import Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    def get_logger(self):
        ...


class RepositoriesProvider(Provider):
    @provide(scope=Scope.APP)
    def get_mongodb_repository(self):
        ...
