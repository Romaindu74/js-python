import json
from typing import Optional
from .Typing.main    import WebSocket as _WebSocket
from .Typing.Typing  import SendDataType, ReceiveDataType

class Context:
    def __init__(self, require, info: dict) -> None:
        self.require = require
        self.info    = info

    def setattr(self, funcs: dict[str, callable]):
        for name in funcs:
            method = funcs[name]

            if not callable(method):
                raise ValueError(f"{method} is not callable")

            setattr(self, name, method)

class require:
    _insitance = None

    modules: dict[str, dict] = {}

    def __new__(cls, ws: Optional[_WebSocket] = None):
        if cls._insitance is None:
            cls._insitance     = super().__new__(cls)
            cls.ws: _WebSocket = ws
    
        return cls._insitance

    def __call__(self, id: str) -> Context:
        info: dict = self.ws.Promise({
            "event": "get-module-info",
            "id": id
        })

        if info.get("code", "js") == "python":
            pass

        else:
            context = Context(self, info)
            funcs   = {}

            for func in info.get("functions", []):
                funcs[func] = lambda *args: self.call(id, func, *args)

            context.setattr(funcs)

            self.modules[id] = {
                "context": context,
                "funcs":   funcs
            }

        return context

    def call(self, id: str, name_func: str, *args: SendDataType) -> SendDataType:
        return self.ws.Promise({
            "event": "execute",
            "module": id,
            "func": name_func,
            "data": args
        })