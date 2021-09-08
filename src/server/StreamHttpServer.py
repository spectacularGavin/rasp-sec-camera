from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from StreamHttpHandler import StreamHttpHandlerFactory
import io
from Configuration import Configuration

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))
indexFile = os.path.join(__location__, 'index.html')
jsmpgFile = os.path.join(__location__, 'jsmpeg.js')

class StreamHttpServer(HTTPServer):
    def __init__(
        self, 
        conf:Configuration
    ):
        super(StreamHttpServer, self).__init__(('', conf.HTTP_PORT), StreamHttpHandlerFactory(conf))
        print(indexFile)
        with io.open(indexFile, 'r') as f:
            self.index_template = f.read()
        with io.open(jsmpgFile, 'r') as f:
            self.jsmpg_content = f.read()