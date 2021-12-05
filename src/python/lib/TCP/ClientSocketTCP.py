import logging

from lib.RawSocket import RawSocket
from lib.TCP.SocketTCP import SocketTCP

class ClientSocket(SocketTCP):
    def connect(self) -> None:
        if not self.socket:
            self.socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "TCP")
            self.socket.connect(self.host, self.port)
            logging.info('Using TCP socket')
        
        