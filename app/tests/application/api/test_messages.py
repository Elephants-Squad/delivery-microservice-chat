from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from mimesis import Text
from httpx import Response


@pytest.mark.asyncio
async def test_create_chat_success(
        test_app: FastAPI,
        client: TestClient,
        test_text: Text,
):
    url = test_app.url_path_for('create_chat_handler')
    title = test_text.text()[:10]
    response: Response = client.post(url=url, json={'title': title})

    assert response.is_success
    json_data = response.json()

    assert json_data['title'] == title


@pytest.mark.asyncio
async def test_create_chat_fail_text_too_long(
        test_app: FastAPI,
        client: TestClient,
        test_text: Text,
):
    url = test_app.url_path_for('create_chat_handler')
    title = test_text.text(quantity=10)
    response: Response = client.post(url=url, json={'title': title})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_create_chat_fail_text_empty(
        test_app: FastAPI,
        client: TestClient,
):
    url = test_app.url_path_for('create_chat_handler')
    response: Response = client.post(url=url, json={'title': ''})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']
