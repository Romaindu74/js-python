from typing import Self, Any, Callable, Union

from .Cog     import Cog
from .Context import Context

from .WebSocket import WebSocket
from .Typing    import ReceiveDataType

class Commands:
    instance:  Self
    commandes: dict[str, Any]

    def __new__(cls)                                                 -> Self:...

    def register(self, name: str, func: Callable, *args)             -> None:...

    @classmethod
    def invoke(cls, name: str, data: ReceiveDataType, ws: WebSocket) -> bool:...

class Command:
    def __init__(self, callback: Callable, **kwargs) -> None:...

    @property
    def cog(self)                                    -> Union[Cog, None]:...
    @cog.setter
    def cog(self, cog: Cog)                          -> None:...

    def __new__(cls, *args, **kwargs)                -> Self:...

    def invoke(self, ctx: Context, *args: Any)       -> Any:...
    
    __call__ = invoke

def command(**attrs)              -> Callable:
    def decorator(func: Callable) -> Command:...
