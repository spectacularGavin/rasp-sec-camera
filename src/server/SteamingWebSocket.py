from ws4py.websocket import WebSocket
from struct import Struct

from Configuration import Configuration

def StreamingWebSocketFactory(config: Configuration):
    class StreamingWebSocket(WebSocket):
        def opened(self):
            print('StreamingWebSocket opened')
            self.send(config.JSMPEG_HEADER.pack(config.JSMPEG_MAGIC, config.WIDTH, config.HEIGHT), binary=True)
        
        def received_message(self, message):
            self.send(u"You said: " + message)

        def closed(self, code):
            print("WebSocket closed. Code: %d"  % code)
    return StreamingWebSocket