import logging
import platform
from importlib import metadata
from typing import Awaitable, Dict, Optional, Union

import httpx

from teler.resources.calls import (
    AsyncCallResourceManager,
    BaseResourceManager,
    CallResourceManager,
)

from . import constants, exceptions

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
        client: httpx.BaseClient,
        headers: Union[Optional[Dict[str, str]], None] = None,
        transport: Union[httpx.BaseTransport, None] = None,
        api_key: str = None,
        calls: BaseResourceManager = None,
        **kwargs,
    ):
        if not api_key:
            raise exceptions.BadParametersException(
                param="api_key", msg="api_key is a required param"
            )
        self.api_key = api_key
        self._client = client(
            transport=transport,
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

    def __init__(self, api_key: str = None):
        super().__init__(
            client=httpx.Client,
            api_key=api_key,
            calls=CallResourceManager,
        )

    def request(self, *args, **kwargs) -> httpx.Response:
        return self._client.request(*args, **kwargs)


class AsyncClient(BaseClient):
    """Asynchronous API Client."""

    def __init__(self, api_key: str = None):
        super().__init__(
            client=httpx.AsyncClient,
            api_key=api_key,
            calls=AsyncCallResourceManager,
        )

    async def request(self, *args, **kwargs) -> Awaitable[httpx.Response]:
        return await self._client.request(*args, **kwargs)
