from lib.Socket import Socket
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM

class ClientSocket(Socket):
    def connect(self) -> None:
        if not self.socket:
            self.socket = socket(AF_INET6 if ":" in self.host else AF_INET, SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))