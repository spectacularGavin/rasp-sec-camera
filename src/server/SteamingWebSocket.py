from ws4py.websocket import WebSocket
from struct import Struct

from Configuration import Configuration

def StreamingWebSocketFactory(config: Configuration):
    class StreamingWebSocket(WebSocket):
        def opened(self):
            self.send(config.JSMPEG_HEADER.pack(config.JSMPEG_MAGIC, config.WIDTH, config.HEIGHT), binary=True)
        # def opened(self, JSMPEG_HEADER: Struct, JSMPEG_MAGIC: bytes, WIDTH: int, HEIGHT: int):
        #     self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)
    return StreamingWebSocket