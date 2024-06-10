from typing import Any, TypeVar, Union

ReplyDataType   = Union[dict, str, list, bool, int, float]
SendDataType    = Union[dict, str, list, bool, int, float]

class __ReceiveDataType:
    reponse:   bool
    data:      SendDataType
    mid:       int

    timestamp: str
    type:      str

ReceiveDataType = __ReceiveDataType

WebSocket = TypeVar("WebSocket")

class Module:
    def setup(self, ws: WebSocket)      -> bool:...
    def execute(self, *args, **kwargs)  -> Any:...
    def run(self, *args, **kwargs)      -> Any:...