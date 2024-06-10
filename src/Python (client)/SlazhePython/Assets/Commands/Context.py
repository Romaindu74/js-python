from typing import Any, Optional

from SlazhePython.Assets.Typing.Typing    import ReceiveDataType, ReplyDataType
from SlazhePython.Assets.Typing.WebSocket import WebSocket

__all__ = (
    "Context"
)

class Context:
    def __init__(self, data: ReceiveDataType, ws: WebSocket) -> None:
        self.ws:   WebSocket       = ws
        self.data: ReceiveDataType = data

    def __call__(self, data: ReplyDataType, type: Optional[str] = "message", reponse: Optional[bool] = False) -> Any:
        if not reponse:
            return self.ws._send(data, reponse, type)
        
    reply = send = __call__