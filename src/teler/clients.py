import logging
import platform
from importlib import metadata
from typing import Dict, Optional, Union

import constants
import exceptions
import httpx

from teler.resources.calls import (
    AsyncCallResourceManager,
    CallResourceManager,
    BaseResourceManager,
)

try:
    __version__ = metadata.version("teler")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

logger = logging.getLogger(__name__)

DEFAULT_REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": f"teler/{__version__} ({platform.machine()} {platform.system().lower()}) Python/{platform.python_version()}",
}


class BaseClient:
    """Base API Client Interface.

    Provides utility methods for interacting with Teler's REST API.
    """

    def __init__(
        self,
        client: Union[httpx.Client, httpx.AsyncClient],
        headers: Optional[Dict[str, str]] = None,
        api_key: str = None,
        calls: BaseResourceManager = None,
        **kwargs,
    ):
        if not api_key:
            raise exceptions.BadParametersException(
                param="api_key", msg="api_key is a required param"
            )
        self.api_key = api_key
        self.client = client(
            base_url=constants.TELER_BASE_URL,
            headers={
                k.lower(): v
                for k, v in {**(headers or {}), **(DEFAULT_REQUEST_HEADERS)}.items()
            },
            **kwargs,
        )
        self.calls = calls


class Client(BaseClient):
    """Synchronous API Client."""

    def __init__(self, api_key: str = ""):
        super().__init__(
            client=httpx.Client,
            api_key=api_key,
            calls=CallResourceManager,
        )

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.client.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.client.delete(*args, **kwargs)


class AsyncClient(BaseClient):
    """Asynchronous API Client."""

    def __init__(self, api_key: str = ""):
        super().__init__(
            client=httpx.AsyncClient,
            api_key=api_key,
            calls=AsyncCallResourceManager,
        )

    async def get(self, *args, **kwargs):
        return await self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.client.post(*args, **kwargs)

    async def patch(self, *args, **kwargs):
        return await self.client.patch(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.client.delete(*args, **kwargs)
