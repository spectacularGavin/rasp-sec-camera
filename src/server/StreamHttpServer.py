from http.server import HTTPServer, BaseHTTPRequestHandler
from StreamHttpHandler import StreamHttpHandler
import io

class StreamHttpServer(HTTPServer):
    def __init__(self, HTTP_PORT:int):
        super(StreamHttpHandler, self).__init__(
                ('', HTTP_PORT), StreamHttpHandler)
        with io.open('index.html', 'r') as f:
            self.index_template = f.read()
        with io.open('jsmpg.js', 'r') as f:
            self.jsmpg_content = f.read()