import time, threading

from SlazhePython import WebSocket, Cog, command, ctx

class Ping(Cog):
    def __init__(self, ws: WebSocket) -> None:
        self.ws: WebSocket = ws

        threading.Thread(target=self.execute).start()

    @command()
    def ping(self, ctx: ctx) -> None:
        data = ctx.data["data"]["time"]

        self.ws.ping.append(time.monotonic() - data)

    def execute(self) -> None:
        while not self.ws.started:
            pass

        while self.ws.keep_running:
            self.ws.WebSocket._send({
                "time": time.monotonic()
            }, True, "ping")

            time.sleep(1)

def setup(ws: WebSocket):
    Ping(ws)

    return True