from fastapi import FastAPI
from punq import Container
from fastapi.testclient import TestClient
from pytest import fixture
from app.application.api.main import app
from app.tests.conftest import container
from mimesis import Text


@fixture
def test_app(container: Container) -> FastAPI:
    app.state.ioc_container = container
    return app


@fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(app=test_app)


@fixture
def test_text() -> Text:
    return Text()
