from typing import Any

import aiohttp
import pytest_asyncio

from tests.config.settings import test_settings


@pytest_asyncio.fixture
async def make_post_request():
    # Make post request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            trust_env=True,
        )

        async with session.post(url, json=query_data) as response:
            status = response.status
            body = await response.json()
        return body, status

    return inner


@pytest_asyncio.fixture
async def make_get_request():
    # Make get request
    async def inner(
        path: str,
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            trust_env=True,
        )

        async with session.get(url) as response:
            status = response.status
            body = await response.json()
        return body, status

    return inner


@pytest_asyncio.fixture
async def make_put_request():
    # Make put request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            trust_env=True,
        )

        async with session.put(url, json=query_data) as response:
            status = response.status
            body = await response.json()
        return body, status

    return inner


@pytest_asyncio.fixture
async def make_delete_request():
    # Make delete request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            trust_env=True,
        )

        async with session.delete(url, json=query_data) as response:
            status = response.status
            body = await response.json()
        return body, status

    return inner
