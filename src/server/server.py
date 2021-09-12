# Taken from https://github.com/waveform80/pistreaming/blob/master/server.py.
# Moved classes to it's own files
from subprocess import Popen, PIPE
from string import Template
from struct import Struct
from threading import Thread
from time import sleep, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from wsgiref.simple_server import make_server
import picamera
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import (
    WSGIServer,
    WebSocketWSGIHandler,
    WebSocketWSGIRequestHandler,
)
from BroadcastOutput import BroadcastOutput
from BroadcastThread import BroadcastThread
from Configuration import Configuration

from SteamingWebSocket import StreamingWebSocketFactory
from StreamHttpServer import StreamHttpServer

###########################################
# CONFIGURATION
WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
VFLIP = False
HFLIP = False

###########################################
# Config object so that it's easier to pass around
CONFIG = Configuration(
    WIDTH,
    HEIGHT ,
    FRAMERATE ,
    HTTP_PORT ,
    WS_PORT ,
    COLOR ,
    BGCOLOR ,
    JSMPEG_MAGIC ,
    JSMPEG_HEADER ,
    VFLIP,
    HFLIP
)

###########################################

def wsFactory():
    WebSocketWSGIHandler.http_version = '1.1'
    websocket_server = make_server(
        '', WS_PORT,
        server_class=WSGIServer,
        handler_class=WebSocketWSGIRequestHandler,
        app=WebSocketWSGIApplication(handler_cls=StreamingWebSocketFactory(CONFIG)))
    websocket_server.initialize_websockets_manager()
    print('Creating websocket at %d' % WS_PORT)
    # websocket_server.initialize_websockets_manager()
    return websocket_server

def httpFactory():
    return StreamHttpServer(CONFIG);

def broadcastFactory(camera: picamera.PiCamera):
    return BroadcastOutput(camera);

def main():
    print('Intializing Camera')
    # ////
    print(CONFIG);
    with picamera.PiCamera() as camera:
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMERATE
        camera.vflip = VFLIP # flips image rightside up, as needed
        camera.hflip = HFLIP # flips image left-right, as needed
        sleep(2) # camera warm-up time
        print('Initializing websockets server on port %d' % WS_PORT)
        websocket_server = wsFactory()
        websocket_thread = Thread(target=websocket_server.serve_forever)

        print('Initializing HTTP server on port %d' % HTTP_PORT)
        http_server = httpFactory()
        http_thread = Thread(target=http_server.serve_forever)
        print('Initializing broadcast thread')
        output = broadcastFactory(camera)
        broadcast_thread = BroadcastThread(output.converter, websocket_server)
        print('Starting recording')
        camera.start_recording(output, 'yuv')

        try:
            print('Starting websockets thread')
            websocket_thread.start()
            print('Starting HTTP server thread')
            http_thread.start()
            print('Starting broadcast thread')
            broadcast_thread.start()
            while True:
                camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            print('Stopping recording')
            camera.stop_recording()
            print('Waiting for broadcast thread to finish')
            broadcast_thread.join()
            print('Shutting down HTTP server')
            http_server.shutdown()
            print('Shutting down websockets server')
            websocket_server.shutdown()
            print('Waiting for HTTP server thread to finish')
            http_thread.join()
            print('Waiting for websockets thread to finish')
            websocket_thread.join()




if __name__ == '__main__':
    main()