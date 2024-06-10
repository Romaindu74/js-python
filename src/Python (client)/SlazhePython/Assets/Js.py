from .Typing.main    import WebSocket as _WebSocket
from .Typing.Typing  import SendDataType, ReceiveDataType

import json

class Js:
    def __init__(self, ws: _WebSocket):
        self.ws: _WebSocket = ws
    
    def __call__(self, func: str, *args: SendDataType) -> ReceiveDataType:
        return self.call(func, *args)

    def call(self, func: str, *args: SendDataType) -> ReceiveDataType:
        self.ws.Promise(json.dumps({
            "event": "call-js",
            "func": func,
            "args": args
        }))
        return 