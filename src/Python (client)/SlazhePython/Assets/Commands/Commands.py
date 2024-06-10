import asyncio

from SlazhePython.Assets.Typing.Typing    import ReceiveDataType
from SlazhePython.Assets.Typing.WebSocket import WebSocket
from SlazhePython.Assets.Typing.Context   import Context as _Context
from SlazhePython.Assets.Typing.Commands  import Command as _Command
from SlazhePython.Assets.Typing.Cog       import Cog     as _Cog
from SlazhePython.Log                     import Logger, Code

from .Context import Context

from typing import Self, Any, Callable, Union

__all__ = (
    "Commands",
    "command"
)

class Commands:
    instance:  Self = None
    commandes: dict[str, _Command] = {}

    def __new__(cls) -> Self:
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def register(self, name: str, func: Callable, *args) -> None:
        Logger.Info(Code("0.0.0.18", _name = __name__, name = name))
        self.commandes[name] = func

    @classmethod
    def invoke(cls, name: str, data: ReceiveDataType, ws: WebSocket):
        if cls.commandes.get(name, None) is None:
            return False

        ctx: _Context = Context(data, ws)

        callback: _Command = cls.commandes.get(name)

        try:
            callback.invoke(ctx)
        except Exception as e:
            Logger.Info(Code("0.0.0.9", _name = __name__, error = str(e)))
        
        else:
            return True

class Command:
    def __init__(self, callback: Callable, **kwargs) -> None:
        if asyncio.iscoroutinefunction(callback):
            raise TypeError('Callback musn\'t be a coroutine.')

        name = kwargs.get('name') or callback.__name__

        if not isinstance(name, str):
            Logger.Error(Code("0.0.0.17", _name = __name__))

        self.name: str = name

        self.callback  = callback
        self._cog: _Cog = None

        self.enabled: bool = kwargs.get('enabled', True)

        Commands().register(self.name, self)

    @property
    def cog(self) -> Union[_Cog, None]:
        return self._cog or None

    @cog.setter
    def cog(self, cog: _Cog) -> None:
        self._cog = cog

    def __new__(cls, *args, **kwargs) -> Self:
        return super().__new__(cls)

    def invoke(self, ctx: _Context, *args: Any) -> None:
        if self.cog is None or ctx is None:
            return
        
        return self.callback(self.cog, ctx, *args)
    
    __call__ = invoke

def command(**attrs) -> Callable:
    def decorator(func: Callable) -> Any:
        return Command(func, **attrs)
    return decorator