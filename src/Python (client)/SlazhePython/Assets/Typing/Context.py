from .Typing    import ReceiveDataType, ReplyDataType
from .WebSocket import WebSocket

from typing import Any, Optional

class Context:
    ws:   WebSocket
    data: ReceiveDataType

    def __init__(self, data: ReceiveDataType, ws: WebSocket) -> None:...
    def __call__(self, data: ReplyDataType, type: Optional[str], reponse: Optional[bool]) -> Any:...