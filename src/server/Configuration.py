from struct import Struct

class Configuration:
    def __init__(
        self,
        WIDTH: int,
        HEIGHT: int,
        FRAMERATE: int,
        HTTP_PORT: int,
        WS_PORT :int,
        COLOR : str,
        BGCOLOR : str,
        JSMPEG_MAGIC : bytes,
        JSMPEG_HEADER : Struct,
        VFLIP: bool,
        HFLIP:bool
    ):
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.FRAMERATE=FRAMERATE
        self.HTTP_PORT=HTTP_PORT
        self.WS_PORT=WS_PORT
        self.COLOR=COLOR
        self.BGCOLOR=BGCOLOR
        self.JSMPEG_MAGIC=JSMPEG_MAGIC
        self.JSMPEG_HEADER=JSMPEG_HEADER
        self.VFLIP=VFLIP
        self.HFLIP=HFLIP

    def __str__(self): 
        return """Configuration: FRAMERATE is % d, 
        HTTP_PORT: % d
        WS_PORT: % d
        """ % (self.FRAMERATE, self.HTTP_PORT, self.WS_PORT) 