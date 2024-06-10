from typing    import Any, Callable, Optional, Union, Literal
from .Typing   import Module as _Module, SendDataType, ReceiveDataType
from .Js       import Js as _Js

import threading

class ABNF:
    OPCODE_TEXT: Literal[1] = 0x1

class _WebSocketApp:
    on_message: Callable
    on_close  : Callable
    on_open   : Callable
    on_error  : Callable

    keep_running: bool

    def run_forever(
        self,
        sockopt: tuple = None,
        sslopt: dict = None,
        ping_interval: float | int = 0,
        ping_timeout: float | int | None = None,
        ping_payload: str = "",
        http_proxy_host: str = None,
        http_proxy_port: int | str = None,
        http_no_proxy: list = None,
        http_proxy_auth: tuple = None,
        http_proxy_timeout: float | None = None,
        skip_utf8_validation: bool = False,
        host: str = None,
        origin: str = None,
        dispatcher: Any | None = None,
        suppress_origin: bool = False,
        proxy_type: str = None,
        reconnect: int = None
    ) -> bool:...

    def send(
        self,
        data: bytes | str,
        opcode: int = ABNF.OPCODE_TEXT
    ) -> None:...

    def close(self, **kwargs: Any) -> None:...


class WebSocket(threading.Thread):
    ws:         _WebSocketApp
    js:         _Js

    key:        str
    method:     str
    uuid:       str
    name:       str

    keyset:     bool

    events:     dict[str, Callable]
    _events:    dict[str, _Module]

    mid:        int
    recv_char:  int
    send_char:  int
    start_time: int

    ping:       list[float]

    def decrypt_data(self, data: str)                                                                                   -> dict[str, Union[str, int, dict, tuple]]:...
    def encrypt_data(self, data: dict[str, Union[str, int, dict, tuple]])                                               -> str:...
    def prepare_data(self, data: Union[str, dict], reponse: Optional[bool] = False, type: Optional[str] = "message")    -> str:...
    def _send(self, data: Union[str, dict], reponse: Optional[bool] = False, type: Optional[str] = "message")           -> bool:...

    def promise(self, data: SendDataType, type: Optional[str] = "message")                                              -> dict[ReceiveDataType]:...

    def __init__(self, url: str)                                                                                        -> None:...
    def run(self)                                                                                                       -> None:...
    def adds_events(self)                                                                                               -> None:...
    def on_message(self, ws: _WebSocketApp, msg: str)                                                                   -> None:...
    def on_close(self, ws: _WebSocketApp, close_status_code: Any, close_reason: Any)                                    -> None:...
    def on_open(self, ws: _WebSocketApp)                                                                                -> None:...
    def on_error(self, ws: _WebSocketApp, error: Any)                                                                   -> None:...
    def setKey(self, file: str, key: str = Any)                                                                         -> None:...
    def setEvent(self, event: str, callback: Callable)                                                                  -> None:...
    def close(self)                                                                                                     -> None:...

    @property
    def get_uuid(self)                                                                                                  -> str:...
    @property
    def get_mid(self)                                                                                                   -> int:...
    @property
    def get_time(self)                                                                                                  -> int:...