from lib.Socket import Socket
import logging

class SocketUDP(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.timeout = 10
    
    def connect(self) -> None:
        super().connect()
        logging.info('Using UDP socket')
        self.socket.settimeout(self.timeout)
