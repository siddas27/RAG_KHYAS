from http.client import HTTPConnection, IncompleteRead
from urllib.parse import urlparse

from threading import Thread
from time import sleep

class MJPEGClientIterator:
    """An iterable producing JPEG-encoded video frames from an MJPEG stream URL."""


    def __init__(self, url):

        o = urlparse(url)

        h = HTTPConnection(o.hostname, port=o.port)

        h.request('GET', o.path)

        response = h.getresponse()

        if response.status == 200:
            self.response = response
            mimetype, options = response.headers['Content-Type'].split("; ")
            self._boundary = options.split("=")[1]

            # print(mimetype, self._boundary)

        else:
            raise Exception("HTTP %d: %s" % (response.status, response.reason))

    def __iter__(self):
        """Yields JPEG-encoded video frames."""

        # TODO: handle chunked encoding delimited by marker instead
        # of content-length.

        while True:
            length = None
            #if line == (self._boundary+"\r\n").encode('ascii'):
            while True:
                l = self.response.fp.readline()
                # print("Chunk start")
                # l = self.response.fp.readline()
                # l = self.response.fp.readline()
                # print(l)

                if l.startswith(b"Content-Length:"):
                    length = int(l.split(b" ")[1])
                    # print("found length", length)

                if length is not None and l== b"\r\n":
                    break

            yield self.response.fp.read(length)
                
                # Look for an empty line, signifying the end of the headers.

class MJPEGClient:
    def __init__(self, url):
        self.url = url
        self.__frame = None

        self.__run = False

    def start(self):
        self.__run = True

        self.__client = iter(MJPEGClientIterator(self.url))
        
        self.__t = Thread(target=self.update)
        self.__t.daemon = True
        self.__t.start()


    def update(self):
        while self.__run:
            self.__frame = next(self.__client)

    def stop(self):
        self.__run = False

    def __iter__(self):
        while self.__run and not self.__frame:
            sleep(1)
        
        while True:
            yield self.__frame
    