import httpx
from typing import Optional, Dict

from teler import constants, exceptions
from teler.resources.calls import (
    AsyncCallResourceManager,
    CallResourceManager,
)

from importlib import metadata

try:
    __version__ = metadata.version("teler")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

DEFAULT_REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": f"teler/{__version__} (python-sdk)",
}


class Client:
    """
    Synchronous HTTP Client for the Teler API.

    Usage:
        with Client(api_key="...") as client:
            ...
    """
    def __init__(self, api_key: str = "", headers: Optional[Dict[str, str]] = None, **kwargs):
        """
        Initialize the synchronous Teler API client.

        Args:
            api_key (str): The API key for authentication.
            headers (Optional[Dict[str, str]]): Additional headers to include in requests.
            **kwargs: Additional arguments passed to httpx.Client.
        """
        if not api_key:
            raise exceptions.BadParametersException("api_key is required")
        self.api_key = api_key
        merged_headers = {
            **(headers or {}),
            **DEFAULT_REQUEST_HEADERS,
            "X-Api-Key": self.api_key,
        }
        self.httpx_client = httpx.Client(
            base_url=constants.TELER_BASE_URL,
            headers={
                k.lower(): v
                for k, v in merged_headers.items()
            },
            **kwargs,
        )
        self.calls = CallResourceManager(self)

    def request(self, *args, **kwargs) -> httpx.Response:
        """
        Make a synchronous HTTP request using the underlying httpx.Client.
        """
        return self.httpx_client.request(*args, **kwargs)

    def close(self):
        """
        Close the underlying httpx.Client.
        """
        self.httpx_client.close()

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close the client.
        """
        self.close()


class AsyncClient:
    """
    Asynchronous HTTP Client for the Teler API.

    Usage:
        async with AsyncClient(api_key="...") as client:
            ...
    """
    def __init__(self, api_key: str = "", headers: Optional[Dict[str, str]] = None, **kwargs):
        """
        Initialize the asynchronous Teler API client.

        Args:
            api_key (str): The API key for authentication.
            headers (Optional[Dict[str, str]]): Additional headers to include in requests.
            **kwargs: Additional arguments passed to httpx.AsyncClient.
        """
        if not api_key:
            raise exceptions.BadParametersException("api_key is required")
        self.api_key = api_key
        merged_headers = {
            **(headers or {}),
            **DEFAULT_REQUEST_HEADERS,
            "X-Api-Key": self.api_key,
        }
        self.httpx_client = httpx.AsyncClient(
            base_url=constants.TELER_BASE_URL,
            headers={
                k.lower(): v
                for k, v in merged_headers.items()
            },
            **kwargs,
        )
        self.calls = AsyncCallResourceManager(self)

    async def request(self, *args, **kwargs) -> httpx.Response:
        """
        Make an asynchronous HTTP request using the underlying httpx.AsyncClient.
        """
        return await self.httpx_client.request(*args, **kwargs)

    async def aclose(self):
        """
        Close the underlying httpx.AsyncClient.
        """
        await self.httpx_client.aclose()

    async def __aenter__(self):
        """
        Enter the async runtime context related to this object.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the async runtime context and close the client.
        """
        await self.aclose()
