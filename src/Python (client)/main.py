from SlazhePython   import WebSocket

from Events import ping, info

if __name__ == "__main__":
    ws = WebSocket()

    ws.init("ws://localhost:8765")

    ws.setName("Programe-1")
    ws.set_queue()

    def msg(msg: str) -> None:
        print(msg)

    ws.on_Message(msg)

    ws.start("./key/Test.key", "salut-e ?")
    ws.attemp_running()

    ping.setup(ws)
    info.setup(ws)
