import httpx
import pytest

from teler import AsyncClient, Client, exceptions
from teler.resources.calls import AsyncCallResourceManager, CallResourceManager

TEST_API_KEY = "TEST_API_KEY"


# Sync client
def test_client_init_sets_api_key_and_client_and_managers():
    client = Client(api_key=TEST_API_KEY)

    assert client.api_key == TEST_API_KEY
    assert isinstance(client._client, httpx.Client)
    assert client.calls is CallResourceManager


def test_client_init_missing_api_key_raises():
    with pytest.raises(exceptions.BadParametersException):
        Client()


# Async client
@pytest.mark.asyncio
async def test_async_client_init_sets_api_key_and_client_and_managers():
    client = AsyncClient(api_key=TEST_API_KEY)

    assert client.api_key == TEST_API_KEY
    assert isinstance(client._client, httpx.AsyncClient)
    assert client.calls is AsyncCallResourceManager

    await client._client.aclose()


@pytest.mark.asyncio
async def test_async_client_init_missing_api_key_raises():
    with pytest.raises(exceptions.BadParametersException):
        AsyncClient()
