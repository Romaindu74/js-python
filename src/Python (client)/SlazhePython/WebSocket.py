from .Assets.Typing.WebSocket   import _WebSocketApp
from .Assets.Typing.Typing      import SendDataType, ReceiveDataType

from .Assets.Libs               import Js
from .Assets.Promise            import Promise
from .Assets.Commands.Commands  import Commands

from .Log                       import Logger, Code

from typing    import Any, Callable, Union, Optional
from websocket import WebSocketApp

import random, threading, json, time

__all__ = (
    "WebSocket"
)

class WebSocket(threading.Thread):
    def __init__(self, url: str) -> None:
        threading.Thread.__init__(self)

        self.ws: _WebSocketApp = WebSocketApp(url)

        self.ws.on_message = self.on_message
        self.ws.on_close   = self.on_close
        self.ws.on_open    = self.on_open
        self.ws.on_error   = self.on_error

        self.js:     Js    = Js()

        self.mid:    int   = 0

        self.key:    str
        self.method: str

        self.keyset: bool  = False

        self.events:  dict[str, Callable]  = {}
        self._events: dict[str, Any]       = {}
        self.__promise: dict[str, Promise] = {}

        self.recv_char: int = 0
        self.send_char: int = 0

        self.start_time: int = self.get_time

        self.ping: list[float] = []

        Logger.Info(Code("0.0.0.6", _name = __name__))
        self.uuid: str = self.get_uuid()
        Logger.Info(Code("0.0.0.7", _name = __name__, uuid = self.uuid))

        self.name: str = "undefined"

    def get_uuid(self):
        return '-'.join([
             (''.join([
            '%x' % random.randint(0, 15) for _ in range(8)
        ])), (''.join([
            '%x' % random.randint(0, 15) for _ in range(4)
        ])), (''.join([
            '%x' % random.randint(0, 15) for _ in range(3)
        ])), (''.join([
            '%x' % (random.randint(0, 3) | 8)
        ])), (''.join([
            '%x' % random.randint(0, 15) for _ in range(3)
        ])), (''.join([
            '%x' % random.randint(0, 15) for _ in range(12)
        ]))])

    def run(self):
        Logger.Info(Code("0.0.0.4", _name = __name__))
        threading.Thread(target=self.ws.run_forever).start()

    def on_message(self, ws: _WebSocketApp, msg: str) -> None:
        self.recv_char += len(msg)
        
        data = self.decrypt_data(msg)

        if data.get("type", None) != "logger":
            Logger.Debug(Code("0.0.0.8", _name = __name__))

        if self.__promise.get(data.get("mid", None), None):
            return self.__promise[data.get("mid")].receive(data.get('data', data))

        try:
            Commands.invoke(data["type"], data, self)
        except Exception as e:
            Logger.Info(Code("0.0.0.9", _name = __name__, error = str(e)))

    def on_close(self, ws: _WebSocketApp, close_status_code: Any, close_reason: Any) -> None:
        Logger.Info(Code("0.0.0.10", _name = __name__))
        pass

    def on_open(self, ws: _WebSocketApp) -> None:
        Logger.Info(Code("0.0.0.11", _name = __name__))
        pass

    def on_error(self, ws: _WebSocketApp, error: Any) -> None:
        Logger.Info(Code("0.0.0.12", _name = __name__, error = str(error)))
        pass

    @property
    def get_mid(self) -> int:
        self.mid += 1

        return self.mid

    @property
    def get_time(self) -> int:
        return int(time.time())

    def decrypt_data(self, data: str) -> dict[str, Union[str, int, dict, tuple]]:
        result = data

        for method in list(reversed(self.method.split("-"))):
            for func in self.js.def_receive[method]:
                result = func(result, self.key)

        return json.loads(result)

    def encrypt_data(self, data: dict[str, Union[str, int, dict, tuple]]) -> str:
        result = json.dumps(data)

        for method in self.method.split("-"):
            for func in self.js.def_send[method]:
                result = func(result, self.key)

        return result

    def prepare_data(self, data: SendDataType, reponse: bool = False, type: str = "message") -> Union[str, int]:
        mid = self.get_mid

        return [self.encrypt_data({
            "timestamp": self.get_time,
            "mid": mid,
            "type": type,
            "data": data,
            "reponse": reponse
        }), mid]

    def promise(self, data: SendDataType, type: Optional[str] = "message") -> ReceiveDataType:
        while not self.ws.keep_running:
            time.sleep(0.05)

        result = self.prepare_data(data, True, type)

        __promise = Promise(self, data, result)
        self.__promise[result[1]] = __promise

        if type != "logger":
            Logger.Debug(Code("0.0.0.13", _name = __name__))

        self.ws.send(result[0])

        return __promise.result()

    def _send(self, data: SendDataType, reponse: bool = False, type: str = "message") -> bool:
        result = self.prepare_data(data, reponse, type)

        if type != "logger":
            Logger.Debug(Code("0.0.0.13", _name = __name__))

        try:
            self.ws.send(result[0])
        except:
            return False
        finally:
            self.send_char += len(result[0])

            return True

    def setKey(self, file: str, key: str = Any) -> None:
        result:      str  = file

        Logger.Info(Code("0.0.0.14", _name = __name__))
        for method in ["aes", "zlib"]:
            result = self.js.def_key[method][0](result, key)

        ops: dict[str, str] = json.loads(result)

        self.keyset: bool = True

        Logger.Info(Code("0.0.0.15", _name = __name__))
        self.method: str  = ops['method']
        self.key:    str  = ops['key']

    def setEvent(self, event: str, callback: Callable) -> None:
        Logger.Info(Code("0.0.0.16", _name = __name__, event = event))
        Commands().register(event, callback)

    def close(self) -> None:
        self.ws.close()