from typing import Self, TypeVar

Command = TypeVar("Command")

class MetaCog(type):
    __cog_commands__: dict[str, Command]

    def __new__(cls, *args, **kwargs) -> Self:...

class Cog(metaclass=MetaCog):
    __cog_commands__: dict[str, Command]

    def __new__(cls, *args, **kwargs) -> Self:...