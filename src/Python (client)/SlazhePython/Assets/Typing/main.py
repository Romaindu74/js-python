from .WebSocket import WebSocket as WebSocketApp
from .Typing    import SendDataType, ReceiveDataType

from typing import Self, Optional, Callable

class WebSocket:
    _instance: Self
    WebSocket: WebSocketApp
    path:      str
    uuid:      str

    def __new__(cls, new_instance: Optional[bool]) -> Self:...

    def send(self, text: str)                      -> bool:...
    def send_json(self, data: dict)                -> bool:...

    def Promise(self, text: SendDataType)          -> ReceiveDataType:...

    def init(self, url: str, path: Optional[str])  -> None:...
    def start(self, key: str)                      -> None:...
    def close(self)                                -> None:...
    def on(self, event: str, callback: Callable)   -> None:...
    def on_Message(self, callback: Callable)       -> None:...
    def setName(self, name: str)                   -> None:...

    @property
    def recv_char(self)                            -> int:...
    
    @property
    def send_char(self)                            -> int:...

    @property
    def keep_running(self)                         -> bool:...