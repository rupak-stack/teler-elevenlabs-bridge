from typing import Dict, Any


class CallFlow:

    @staticmethod
    def dial(
        from_number: str,
        to_number: str,
        status_callback_url: str = "",
        record: bool = True,
    ) -> Dict[str, Any]:
        return {
            "action": "dial",
            "from_numebr": from_number,
            "to_number": to_number,
            "status_callback_url": status_callback_url,
            "record": record,
        }

    @staticmethod
    def stream(
        ws_url: str, chunk_size: int = 400, record: bool = True
    ) -> Dict[str, Any]:
        return {
            "action": "stream",
            "ws_url": ws_url,
            "chunk_size": chunk_size,
            "record": record,
        }

    @staticmethod
    def play(file_url: str) -> Dict[str, Any]:
        return {"action": "play", "file_url": file_url}
