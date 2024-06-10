import datetime
from io import TextIOWrapper
import time
import colorama
import sys, threading
import base64, os

from typing             import Any, Self, Union, Optional

from .Assets.Typing.WebSocket import WebSocket as _WebSocket
from .Assets.Typing.Log       import TextLogger

from .Assets.Libs import cwd

colorama.init(True)

CRITICAL  = 50
ERROR     = 40
WARNING   = 30
INFO      = 20
DEBUG     = 10
NOSET     = 0

code = {}

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR:    'ERROR',
    WARNING:  'WARNING',
    INFO:     'INFO',
    DEBUG:    'DEBUG',
    NOSET:    'NOSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'ERROR':    ERROR,
    'WARNING':  WARNING,
    'INFO':     INFO,
    'DEBUG':    DEBUG,
    'NOSET':    NOSET,
}

_nameToColor = {
    'CRITICAL': colorama.Fore.RED,
    'ERROR':    colorama.Fore.RED,
    'WARNING':  colorama.Fore.YELLOW,
    'INFO':     colorama.Fore.GREEN,
    'DEBUG':    colorama.Fore.WHITE,
    'NOSET':    colorama.Fore.WHITE
}

class Code:
    def __init__(self, code: str = '', __default: str = False, _name: Optional[str] = __name__, **options) -> None:
        self.code      = code
        self.__default = __default
        self.options   = options

        self.name      = _name

        if self.code == None:
            self.code = ''

    def __str__(self) -> str:
        return self.code

    def format(self, text: str) -> str:
        if not isinstance(text, str):
            return self.__default
        return base64.b64decode(text).decode('latin-1').format(**self.options)

    def content(self) -> str:
        if code.get(self.code):
            return self.format(code.get(self.code))
        return self.format(Logger.get(self.code, self.__default, **self.options))

class LoggerQueue:
    def __init__(self, text: str, level: int, *args: Any, **kwargs: Any) -> None:
        self.text: str   = text
        self.level: int  = level
        self.args: Any   = args
        self.kwargs: Any = kwargs

class Logger:
    _instance:  Self        = None
    ws:         _WebSocket  = None
    queue:      list[LoggerQueue] = []

    def set_ws(self, ws: _WebSocket) -> None:
        self._instance.ws = ws

    def __new__(cls, path: Optional[str] = cwd(), name: Optional[str] = __name__) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.name = name
            cls.path = path

            threading.Thread(target=cls.loop, args = [cls._instance]).start()

        return cls._instance

    def loop(self) -> None:
        while True:
            if len(self.queue) > 0 and self._instance.ws != None and self._instance.ws.ws.keep_running:
                element = self.queue[0]

                self._print(element.text, element.level, *element.args, **element.kwargs)

                del self.queue[0]

            else:
                time.sleep(0.05)

    @classmethod
    def get(cls, _code: str, __default: Optional[str] = None, **options: Any) -> str:
        global code

        result: TextLogger = cls._instance.ws.promise(_code, "logger")

        if result.get('found', False):
            code[_code] = result.get('text')

            return result.get('text')

        return __default

    def getLevel(self, level: Union[str, int]) -> str:
        if isinstance(level, str):
            return level
        
        return _levelToName.get(level, 'NOSET')

    def color(self, level: str) -> str:
        return _nameToColor.get(level, colorama.Fore.WHITE)

    def strftime(self, format: str) -> str:
        return datetime.datetime.now().strftime(format)

    @property
    def time(self) -> str:
        return self.strftime("%H:%M:%S")

    @property
    def date(self) -> str:
        return self.strftime("%Y-%m-%d")

    def status(self, level: Union[int, str], max: int = 10) -> str:
        level = self.getLevel(level)
        color = self.color(level)

        return color + level + ((max - len(level)) * ' ') + colorama.Fore.WHITE

    def _save(self, text: str, level: int, max: int = 10, name: Optional[str] = None) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        try:
            file: TextIOWrapper = open('{0}/Logs {1}.txt'.format(self.path, self.date), 'a')
        except FileNotFoundError:
            file: TextIOWrapper = open('{0}Logs {1}.txt'.format(self.path, self.date), 'w+')
        except Exception as e:
            raise Exception(e)

        name  = name if name != None else self.name
        level = self.getLevel(level)

        file.write('[{0}] [{1}] [{2}] {3}\n'.format(
                f"{self.date} {self.time}",
                (name + ((45 - len(name)) * ' ')),
                level + (max - len(level)) * ' ',
                str(text)
            ))
        file.close()

    def _print(self, text: Union[str, Code], level: int, *args, **kwargs) -> None:
        if text == None:
            return

        name = self.name

        if isinstance(text, Code):
            name = text.name
            text = text.content()

        context = '[{0}] [{1}] [{2}] {3}'.format(
                f"{self.date} {self.time}",
                (name + ((45 - len(name)) * ' ')),
                self.status(level),
                str(text)
            )

        if kwargs.get('Log', True):
            # print(context)
            pass

        if kwargs.get('Save', True) and level > 10:
            self._save(text, level, name = name)

        if kwargs.get('Exit', False):
            sys.exit(0)

    @classmethod
    def Critical(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, CRITICAL, *args, **kwargs))

    @classmethod
    def Error(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, ERROR, *args, **kwargs))

    @classmethod
    def Warn(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, WARNING, *args, **kwargs))

    @classmethod
    def Info(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, INFO, *args, **kwargs))

    @classmethod
    def Debug(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, DEBUG, *args, **kwargs))

    @classmethod
    def NoSet(cls, text: Union[str, Code] = None, *args, **kwargs) -> None:
        cls.queue.append(LoggerQueue(text, NOSET, *args, **kwargs))


def Log(level: int = 0, text: str = '', _exit: bool = False, **options):
    Logger()._print(text, level, Exit = _exit, **options)
