from ws4py.websocket import WebSocket
from struct import Struct

class StreamingWebSocket(WebSocket):
    def opened(self, JSMPEG_HEADER: Struct, JSMPEG_MAGIC: bytes, WIDTH: int, HEIGHT: int):
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)