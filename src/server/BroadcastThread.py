from threading import Thread
from subprocess import Popen, PIPE
from wsgiref.simple_server import WSGIServer

class BroadcastThread(Thread):
    def __init__(self, converter: Popen, websocket_server: WSGIServer):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.websocket_server = websocket_server

    def run(self):
        print('in BroadcastThread')
        try:
            while True:
                buf = self.converter.stdout.read1(32768)
                if buf:
                    self.websocket_server.manager.broadcast(buf, binary=True)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()