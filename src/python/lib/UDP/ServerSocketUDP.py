import logging
from lib.UDP.SocketUDP import SocketUDP
from lib.RawSocket import RawSocket

class ServerSocket(SocketUDP):
    def connect(self) -> None:
        if not self.socket:
            self.socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "UDP")
            self.socket.bind(self.host, self.port)
            logging.info('Using UDP socket')
    
