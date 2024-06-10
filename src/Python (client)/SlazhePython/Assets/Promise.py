from .Typing.WebSocket import WebSocket as _WebSocket
from .Typing.Typing    import SendDataType, ReceiveDataType

from typing            import Union

import time

class Promise:
    def __init__(self, ws: _WebSocket, data: SendDataType, encrypt_data: Union[str, int]) -> None:
        self.__receive: ReceiveDataType = None

        self.ws: _WebSocket     = ws
        self.data: SendDataType = data

        self.mid: int           = encrypt_data[1]

    def receive(self, data: ReceiveDataType) -> None:
        self.__receive: ReceiveDataType = data

    def result(self) -> ReceiveDataType:
        while not self.__receive:
            time.sleep(0.05)

        return self.__receive