from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from string import Template
from typing import Tuple
from time import sleep, time
from Configuration import Configuration

def StreamHttpHandlerFactory(config: Configuration):
    print(config)
    class StreamHttpHandler(BaseHTTPRequestHandler):
        # def __init__(
        #     self, 
        #     request: bytes, 
        #     client_address: Tuple[str, int], 
        #     server: socketserver.BaseServer
        # ) -> None:
        #     super().__init__(request, client_address, server)

        @property
        def WS_PORT(self):
            return config.WS_PORT

        @property
        def WIDTH(self):
            return config.WIDTH
        
        @property
        def HEIGHT(self):
            return config.HEIGHT
        
        @property
        def COLOR(self):
            return config.COLOR

        @property
        def BGCOLOR(self):
            return config.BGCOLOR

        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
                return
            elif self.path == '/jsmpg.js':
                content_type = 'application/javascript'
                content = self.server.jsmpg_content
            elif self.path == '/index.html':
                content_type = 'text/html; charset=utf-8'
                tpl = Template(self.server.index_template)
                content = tpl.safe_substitute(dict(
                    WS_PORT=self.WS_PORT, WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, COLOR=self.COLOR,
                    BGCOLOR=self.BGCOLOR))
            else:
                self.send_error(404, 'File not found')
                return
            content = content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Last-Modified', self.date_time_string(time()))
            self.end_headers()
            if self.command == 'GET':
                self.wfile.write(content)

    return StreamHttpHandler