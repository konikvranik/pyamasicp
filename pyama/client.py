import logging

BUFFER_SIZE = 1024

class Client:
    def __init__(self, host, port = 5000):
        self._host = host
        self._port = port
        self.logger = logging.getLogger(self.__class__.__name__)