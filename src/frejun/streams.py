import asyncio
from typing import Callable

import exceptions
import websockets


class MediaStreamTypes:
    UNIDIRECTIONAL = 1
    BIDIRECTIONAL = 2


class MediaStreamConnector:
    """
    Media Stream Connector Interface.

    Opens a Websocket connection with `remote_url` and delegates message processing to the caller.
    """

    def _default_call_stream_handler(message, remote_ws):
        remote_ws.send(message)

    def _default_remote_stream_handler(message, call_ws):
        call_ws.send(message)

    def __init__(
        self,
        stream_type: int = MediaStreamTypes.BIDIRECTIONAL,
        remote_url: str = "",
        call_stream_handler: Callable = _default_call_stream_handler,
        remote_stream_handler: Callable = _default_remote_stream_handler,
    ):
        if stream_type == MediaStreamTypes.UNIDIRECTIONAL:
            raise exceptions.NotImplemented(
                msg="Unidirectional media streams are not supported yet."
            )
        if not remote_url:
            raise exceptions.InvalidParameters(
                msg="remote_url is a required parameter."
            )
        self.stream_type = stream_type
        self.remote_url = remote_url
        self.call_stream_handler = call_stream_handler
        self.remote_stream_handler = remote_stream_handler

    async def bridge_stream(self, call_ws):
        async with websockets.connect(self.remote_url) as remote_ws:

            async def call_stream() -> None:
                async for message in call_ws.iter_bytes():
                    await self.call_stream_handler(message, remote_ws)

            async def remote_stream() -> None:
                async for message in remote_ws:
                    await self.remote_stream_handler(message, call_ws)

        done, pending = await asyncio.wait(
            [asyncio.create_task(call_stream()), asyncio.create_task(remote_stream())],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
