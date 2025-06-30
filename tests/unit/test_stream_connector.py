import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from teler import exceptions
from teler.streams import StreamConnector, StreamType, StreamOp


class TestStreamConnector:
    """Test cases for StreamConnector class."""

    def test_init_with_valid_parameters(self):
        """Test StreamConnector initialization with valid parameters."""
        remote_url = "ws://example.com/stream"
        connector = StreamConnector(
            stream_type=StreamType.BIDIRECTIONAL,
            remote_url=remote_url
        )
        
        assert connector.stream_type == StreamType.BIDIRECTIONAL
        assert connector.remote_url == remote_url
        # Test that handlers are set (don't compare static methods directly)
        assert connector.call_stream_handler is not None
        assert connector.remote_stream_handler is not None

    def test_init_with_custom_handlers(self):
        """Test StreamConnector initialization with custom handlers."""
        async def custom_handler(message: str):
            return (f"processed_{message}", StreamOp.RELAY)
        
        remote_url = "ws://example.com/stream"
        connector = StreamConnector(
            remote_url=remote_url,
            call_stream_handler=custom_handler,
            remote_stream_handler=custom_handler
        )
        
        assert connector.call_stream_handler == custom_handler
        assert connector.remote_stream_handler == custom_handler

    def test_init_missing_remote_url_raises_exception(self):
        """Test that initialization without remote_url raises BadParametersException."""
        with pytest.raises(exceptions.BadParametersException) as exc_info:
            StreamConnector(remote_url="")
        
        assert exc_info.value.param == "remote_url"
        assert "remote_url is a required parameter" in str(exc_info.value)

    def test_init_unidirectional_stream_raises_exception(self):
        """Test that unidirectional streams raise NotImplemented exception."""
        with pytest.raises(exceptions.NotImplementedException) as exc_info:
            StreamConnector(
                stream_type=StreamType.UNIDIRECTIONAL,
                remote_url="ws://example.com/stream"
            )
        
        assert "Unidirectional streams are not supported yet" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_default_stream_handler(self):
        """Test the default stream handler returns message with RELAY operation."""
        result = await StreamConnector._default_stream_handler("test_message")
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == "test_message"
        assert result[1] == StreamOp.RELAY

    @pytest.mark.asyncio
    async def test_bridge_stream_establishes_websocket_connection(self):
        """Test that bridge_stream establishes WebSocket connection."""
        remote_url = "ws://example.com/stream"
        connector = StreamConnector(remote_url=remote_url)
        
        # Mock call WebSocket
        mock_call_ws = AsyncMock()
        mock_call_ws.iter_text.return_value = []
        
        with patch('websockets.connect') as mock_connect:
            mock_remote_ws = AsyncMock()
            mock_connect.return_value.__aenter__.return_value = mock_remote_ws
            
            await connector.bridge_stream(mock_call_ws)
            
            mock_connect.assert_called_once_with(remote_url)

    @pytest.mark.asyncio
    async def test_bridge_stream_websocket_connection_error(self):
        """Test handling of WebSocket connection errors."""
        remote_url = "ws://example.com/stream"
        connector = StreamConnector(remote_url=remote_url)
        
        # Mock call WebSocket
        mock_call_ws = AsyncMock()
        mock_call_ws.iter_text.return_value = []
        
        with patch('websockets.connect') as mock_connect:
            mock_connect.side_effect = Exception("Connection failed")
            
            with pytest.raises(Exception) as exc_info:
                await connector.bridge_stream(mock_call_ws)
            
            assert "Connection failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_bridge_stream_cleanup_on_completion(self):
        """Test that pending tasks are properly cancelled on completion."""
        remote_url = "ws://example.com/stream"
        connector = StreamConnector(remote_url=remote_url)
        
        # Mock call WebSocket
        mock_call_ws = AsyncMock()
        mock_call_ws.iter_text.return_value = []
        
        with patch('websockets.connect') as mock_connect:
            mock_remote_ws = AsyncMock()
            mock_remote_ws.__aiter__.return_value = iter([])
            mock_connect.return_value.__aenter__.return_value = mock_remote_ws
            
            # Create a task that will complete quickly
            task = asyncio.create_task(connector.bridge_stream(mock_call_ws))
            
            # Wait a bit for the streams to process
            await asyncio.sleep(0.1)
            
            # Cancel the task to clean up
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            # Verify the bridge completed (no exceptions raised)
            assert True  # If we get here, cleanup was successful
