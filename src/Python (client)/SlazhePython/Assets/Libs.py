def cwd(path: str = __file__) -> str:
    file = ("\\".join(path.split('/'))).split("\\")
    file.pop()

    return "/".join(file) + "/"

try:
    import execjs
except ImportError:
    print("Module 'execjs' n'est pas installer.")

from typing import Callable

from SlazhePython.Assets.Typing.Js import execjsCallable

class Js:
    def __init__(self):
        self.AES:  execjsCallable = execjs.compile((open("./SlazhePython/Assets/Js/aes.js", "r").read()))
        self.ZLIB: execjsCallable = execjs.compile((open("./SlazhePython/Assets/Js/zlib.js", "r").read()))

        self.def_receive: dict[str, list[Callable]] = {
            "zlib": [
                self.Inflate
            ],
            "aes": [
                self.Decrypt
            ]
        }

        self.def_key = self.def_receive

        self.def_send: dict[str, list[Callable]] = {
            "zlib": [
                self.Deflate
            ],
            "aes": [
                self.Encrypt
            ]
        }

    def Encrypt(self, text: str, key: str, *args, **kwargs) -> str:
        return self.AES.call("Encrypt", text, key)

    def Decrypt(self, text: str, key: str, *args, **kwargs) -> str:
        return self.AES.call("Decrypt", text, key)

    def Deflate(self, text: str, *args, **kwargs) -> str:
        return self.ZLIB.call("Deflate", text)

    def Inflate(self, text: str, *args, **kwargs) -> str:
        return self.ZLIB.call("Inflate", text)
