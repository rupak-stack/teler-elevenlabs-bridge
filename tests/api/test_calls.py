import httpx
import pytest
import respx

from teler import AsyncClient, Client
from teler.resources.calls import CallResource


@respx.mock
def test_call_create_hits_route_and_returns_call_resource():
    client = Client(api_key="")
    data = {
        "from_number": "+123456789",
        "to_number": "+123456789",
        "flow_url": "https://api.frejun.ai/flow",
        "status_callback_url": "https://api.frejun.ai/status",
        "record": True,
    }

    route = respx.post("https://api.teler.ai/calls").mock(
        return_value=httpx.Response(201, json={"id": 456})
    )

    call = client.calls.create(**data)

    assert route.called
    assert isinstance(call, CallResource)


@pytest.mark.asyncio
async def test_async_call_create_hits_route_and_returns_call_resource():
    client = AsyncClient(api_key="")
    data = {
        "from_number": "+123456789",
        "to_number": "+987654321",
        "flow_url": "https://api.frejun.ai/flow",
        "status_callback_url": "https://api.frejun.ai/status",
        "record": True,
    }

    route = respx.post("https://api.teler.ai/calls").mock(
        return_value=httpx.Response(201, json={"id": 456})
    )

    call = await client.calls.create(**data)

    assert route.called
    assert isinstance(call, CallResource)
