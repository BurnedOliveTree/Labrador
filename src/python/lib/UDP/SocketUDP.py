from lib.Socket import Socket
import logging

from lib.RawSocket import RawSocket

class SocketUDP(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
    
    def connect(self) -> None:
        if not self.socket:
            self.socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "UDP")
            logging.info('Using UDP socket')