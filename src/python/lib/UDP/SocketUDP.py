from lib.Socket import Socket
import logging

class SocketUDP(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
    
    def create_UDP_socket(self) -> None:
        self.socket = self.create_socket("ipv6" if ":" in self.host else "ipv4", "UDP")
        logging.info('Using UDP socket')
        self.socket.enable_timeout()