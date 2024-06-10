from .Typing.main import WebSocket as _WebSocket

import threading, time, json

class Queue:
    def __init__(self, ws: _WebSocket, max_payload: int = 64000, time_ms: int = 1) -> None:
        self.ws:     _WebSocket = ws

        self.queue:  list[str] = []
        self.max_payload: int  = max_payload
        self.time_ms:     int  = time_ms
        self._stop:       bool = False

        self.thread: threading.Thread = threading.Thread(target = self.loop)

        self.thread.start()

    def loop(self) -> None:
        while not self._stop:
            while (len(self.queue) == 0 or not self.ws.keep_running) and not self._stop:
                time.sleep(0.005)

            index = 0
            id    = 0
            data  = {}

            timeout    = (time.monotonic_ns() * 10**6) + self.time_ms

            while index < self.max_payload and (time.monotonic_ns() * 10**6) < timeout:
                if len(self.queue) == 0:
                    break

                id += 1

                item = self.queue.pop(0)

                index += len(item)

                data[str(id)] = item

            if index != 0 and id != 0:
                self.ws.send(json.dumps({
                    "class": "queue",
                    "data": data
                }))

    def close(self) -> None:
        self._stop = True

    def send(self, data: str) -> bool:
        self.queue.append(data)

        return True