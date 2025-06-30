import httpx
import pytest
import respx

from teler import AsyncClient, Client
from teler.resources.calls import CallResource


def test_call_create_hits_route_and_returns_call_resource():
    with respx.mock(assert_all_called=False) as respx_mock:
        route = respx_mock.post("https://api.frejun.ai/calls/create").mock(
            return_value=httpx.Response(201, json={"id": 456, "uuid": "test-uuid"})
        )
        client = Client(api_key="test_api_key")
        data = {
            "from_number": "+123456789",
            "to_number": "+123456789",
            "flow_url": "https://api.frejun.ai/flow",
            "status_callback_url": "https://api.frejun.ai/status",
            "record": True,
        }

        call = client.calls.create(**data)

        assert route.called
        assert isinstance(call, CallResource)


@pytest.mark.asyncio
async def test_async_call_create_hits_route_and_returns_call_resource():
    with respx.mock(assert_all_called=False) as respx_mock:
        route = respx_mock.post("https://api.frejun.ai/calls/create").mock(
            return_value=httpx.Response(201, json={"id": 456, "uuid": "test-uuid"})
        )
        client = AsyncClient(api_key="test_api_key")
        data = {
            "from_number": "+123456789",
            "to_number": "+987654321",
            "flow_url": "https://api.frejun.ai/flow",
            "status_callback_url": "https://api.frejun.ai/status",
            "record": True,
        }

        call = await client.calls.create(**data)

        assert route.called
        assert isinstance(call, CallResource)
