import asyncio
from enum import Enum
from typing import Callable, Tuple

import websockets

from teler import exceptions


class StreamType(Enum):
    UNIDIRECTIONAL = 0
    BIDIRECTIONAL = 1


class StreamOp(Enum):
    RELAY = 0
    INTERRUPT = 1
    CLEAR = 2
    STOP = 3
    PASS = 4


class StreamConnector:
    """
    Media Stream Connector Interface.

    Opens a Websocket connection with `remote_url` and delegates message processing to the caller.
    """

    def _default_stream_handler(self, message: str) -> Tuple[str, StreamOp]:
        return (message, StreamOp.RELAY)

    def __init__(
        self,
        stream_type: StreamType = StreamType.BIDIRECTIONAL,
        remote_url: str = "",
        call_stream_handler: Callable = _default_stream_handler,
        remote_stream_handler: Callable = _default_stream_handler,
    ):
        if stream_type == StreamType.UNIDIRECTIONAL:
            raise exceptions.NotImplemented(
                msg="Unidirectional streams are not supported yet."
            )
        if not remote_url:
            raise exceptions.InvalidParameters(
                msg="remote_url is a required parameter."
            )
        self.stream_type = stream_type
        self.remote_url = remote_url
        self.call_stream_handler = call_stream_handler
        self.remote_stream_handler = remote_stream_handler

    async def _process_stream_op(self, stream_op: StreamOp, data, send_ws):
        if stream_op == StreamOp.RELAY:
            await send_ws.send(data)
        elif stream_op == StreamOp.INTERRUPT:
            message = {"event": "interrupt", "data": {"chunk_id": data}}
            await send_ws.send(message)
        elif stream_op == StreamOp.CLEAR:
            message = {"event": "clear"}
            await send_ws.send(message)
        elif stream_op == StreamOp.STOP:
            message = {"event": "stop"}
            await send_ws.send(message)
        elif stream_op == StreamOp.PASS:
            pass

    async def bridge_stream(self, call_ws) -> None:
        async with websockets.connect(self.remote_url) as remote_ws:

            async def call_stream() -> None:
                async for message in call_ws.iter_bytes():
                    res = await self.call_stream_handler(message)
                    if not isinstance(res, tuple):
                        raise exceptions.InvalidStreamOperation(
                            msg="Stream handler response must be a tuple of (str, StreamOp)"
                        )
                    await self._process_stream_op(res[1], res[0], remote_ws)

            async def remote_stream() -> None:
                async for message in remote_ws:
                    res = await self.remote_stream_handler(message)
                    if not isinstance(res, tuple):
                        raise exceptions.InvalidStreamOperation(
                            msg="Stream handler response must be a tuple of (str, StreamOp)"
                        )
                    await self._process_stream_op(res[1], res[0], call_ws)

        done, pending = await asyncio.wait(
            [asyncio.create_task(call_stream()), asyncio.create_task(remote_stream())],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
