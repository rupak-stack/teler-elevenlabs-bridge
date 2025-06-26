from dataclasses import dataclass
from typing import Any, Awaitable, Dict
from uuid import UUID

from ..clients import BaseClient
from .base import AsyncBaseResourceManager, BaseResource, BaseResourceManager

PATHS: Dict[str, str] = {
    "create": "/calls",
    "list": "/calls",
    "retrieve": "/calls/{}",
    "update": "/calls/{}",
    "delete": "/calls/{}",
}


@dataclass
class CallResource(BaseResource):
    uuid: UUID

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)


class CallResourceManager(BaseResourceManager):

    def __init__(self, client: BaseClient):
        super().__init__(client, CallResource, PATHS)

    def create(
        self,
        from_number: str,
        to_number: str,
        flow_url: str,
        status_callback_url: str,
        record: bool = True,
    ) -> CallResource:
        data = {
            "from_number": from_number,
            "to_number": to_number,
            "flow_url": flow_url,
            "status_callback_url": status_callback_url,
            "record": record,
        }
        res = self.client.request("POST", "/calls/create", data=data)
        return self.resource(res.json())


class AsyncCallResourceManager(AsyncBaseResourceManager):

    def __init__(self, client: BaseClient):
        super().__init__(client, CallResource, PATHS)

    async def create(
        self,
        from_number: str,
        to_number: str,
        flow_url: str,
        status_callback_url: str,
        record: bool = True,
    ) -> Awaitable[CallResource]:
        data = {
            "from_number": from_number,
            "to_number": to_number,
            "flow_url": flow_url,
            "status_callback_url": status_callback_url,
            "record": record,
        }
        res = await self.client.request("POST", "/calls/create", data=data)
        return self.resource(res.json())
