from SlazhePython import WebSocket, Cog, command, ctx

class Info(Cog):
    def __init__(self, ws: WebSocket) -> None:
        self.ws: WebSocket = ws

    @command()
    def info(self, ctx: ctx, *args) -> None:
        ctx({
            "recv_char": self.ws.recv_char,
            "send_char": self.ws.send_char,
            "start_time": self.ws.start_time,
            "uuid": self.ws.uuid,
            "ping": self.ws.ping,
            "name": self.ws.name
        }, type = "info")


def setup(ws: WebSocket):
    Info(ws)

    return True