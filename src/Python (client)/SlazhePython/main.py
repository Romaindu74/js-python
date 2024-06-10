from .WebSocket   import WebSocket as WebSocketApp
from .Assets.Libs import cwd
from .Log         import Code, Logger
from .Assets      import queue, require

from typing                 import Any, Callable, Self, Optional
from .Assets.Typing.Typing  import SendDataType, ReceiveDataType

import json, os

__all__ = (
    "WebSocket"
)

class WebSocket:
    _instance: Self = None

    def init(self, url: str, path: Optional[str] = cwd()) -> None:
        self.WebSocket: WebSocketApp = WebSocketApp(url)
        self.path:      str          = path
        self._started:  bool         = False

        self.require                 = require.require(self)

        Logger("{0}/Logs/".format(cwd())).set_ws(self.WebSocket)

    def __new__(cls, new_instance: Optional[bool] = False) -> Self:
        if new_instance:
            return super().__new__(cls)

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def recv_char(self) -> int:
        return self.WebSocket.recv_char
    
    @property
    def send_char(self) -> int:
        return self.WebSocket.send_char

    @property
    def start_time(self) -> int:
        return self.WebSocket.start_time

    @property
    def uuid(self) -> str:
        return self.WebSocket.uuid

    @property
    def ping(self) -> list[float]:
        return self.WebSocket.ping

    @property
    def name(self) -> str:
        return self.WebSocket.name

    @property
    def keep_running(self) -> bool:
        return self.WebSocket.ws.keep_running

    @property
    def started(self) -> bool:
        return self._started

    def start(self, file: str, key: str = Any) -> None:
        Logger.Info(Code("0.0.0.1", _name = __name__))
        if not os.path.exists(file) or key == Any:
            return Logger.Error(Code("0.0.0.2", _name = __name__))

        Logger.Info(Code("0.0.0.3", _name = __name__))
        self.WebSocket.setKey(
            (open(file, "r").read()), key
        )

        while not self.WebSocket.keyset:
            pass

        self.WebSocket.start()

        while not self.keep_running:
            pass

        self._started = True

    def set_queue(self, max_payload: Optional[int] = None, time_ms: Optional[int] = None) -> None:
        self.queue = queue.Queue(self, max_payload, time_ms)

    def close(self) -> None:
        Logger.Info(Code("0.0.0.5", _name = __name__))
        if self.queue:
            self.queue.close()

        self.WebSocket.close()

    def on(self, event: str, callback: Callable) -> None:
        self.WebSocket.setEvent(event, callback)

    def on_Message(self, callback: Callable) -> None:
        self.WebSocket.setEvent("message", callback)

    def send(self, text: str) -> bool:
        if not self.keep_running or not self.started:
            return False

        if self.queue:
            return self.queue.send(text)

        return self.WebSocket._send(text)

    def send_json(self, data: dict) -> bool:
        return self.send(json.dumps(data))

    def setName(self, name: str) -> None:
        self.WebSocket.name = name

    def Promise(self, data: SendDataType) -> ReceiveDataType:
        return self.WebSocket.promise(data)

    def attemp_running(self) -> None:
        while not self.started:
            pass

        while not self.keep_running:
            pass