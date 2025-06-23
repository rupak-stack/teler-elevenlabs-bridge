from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Dict, Awaitable, List

import exceptions

from ..clients import BaseClient


@dataclass
class BaseResource(ABC):

    def __init__(self, data):
        # Match only declared fields; raise on extra keys
        names = {f.name for f in fields(self)}
        unknown = set(data) - names
        if unknown:
            raise TypeError(f"Unknown fields: {unknown}")
        for field in names:
            setattr(self, field, data.get(field))


class BaseResourceManager(ABC):

    def __init__(
        self, client: BaseClient, resource: BaseResource, paths: Dict[str, str]
    ):
        self.client = client
        self.resource = resource
        self.paths = paths

    @abstractmethod
    def create(self) -> BaseResource:
        raise exceptions.NotImplementedException(
            msg="Method 'create()' is not implemented."
        )

    def list(self) -> List[BaseResource]:
        res = self.client.get("/calls")
        return self.resource(res.json().data)

    def retrieve(self, id) -> BaseResource:
        res = self.client.delete(self.paths["retrieve"].format(id))
        return self.resource(res.json().data)

    def update(self, id) -> BaseResource:
        res = self.client.delete(self.paths["update"].format(id))
        return self.resource(res.json().data)

    def delete(self, id) -> None:
        _ = self.client.delete(self.paths["delete"].format(id))
        return None


class AsyncBaseResourceManager(ABC):

    def __init__(
        self, client: BaseClient, resource: BaseResource, paths: Dict[str, str]
    ):
        self.client = client
        self.resource = resource
        self.paths = paths

    @abstractmethod
    async def create(self) -> BaseResource:
        raise exceptions.NotImplementedException(
            msg="Method 'create()' is not implemented."
        )

    async def list(self) -> Awaitable[List[BaseResource]]:
        res = await self.client.get(self.paths["list"])
        return self.resource(res.json().data)

    async def retrieve(self, id) -> Awaitable[BaseResource]:
        res = await self.client.get(self.paths["retrieve"].format(id))
        return self.resource(res.json().data)

    async def update(self, id) -> Awaitable[BaseResource]:
        res = await self.client.patch(self.paths["update"].format(id))
        return self.resource(res.json().data)

    async def delete(self, id) -> None:
        _ = await self.client.delete(self.paths["delete"].format(id))
        return None
