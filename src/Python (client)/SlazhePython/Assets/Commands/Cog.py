from .Commands import Command

from typing    import Self

__all__ = (
    'Cog'
)

class MetaCog(type):
    __cog_commands__: dict[str, Command]

    def __new__(cls, *args, **kwargs) -> Self:
        name, bases, attrs = args

        try:
            cog_name = kwargs.pop('name')
        except KeyError:
            cog_name = name

        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)
        commands: dict[str, Command] = {}

        for base in reversed(new_cls.__mro__):
            for elem, value in base.__dict__.items():
                is_static_method = isinstance(value, staticmethod)
                if is_static_method:
                    value = value.__func__

                if isinstance(value, Command):
                    commands[elem] = value

        new_cls.__cog_commands__ = commands

        return new_cls

class Cog(metaclass=MetaCog):
    __cog_commands__: dict[str, Command]

    def __new__(cls, *args, **kwargs) -> Self:
        self = super().__new__(cls)

        self.__cog_commands__ = cls.__cog_commands__

        for command in list(self.__cog_commands__.values()):
            command.cog = self

        return self