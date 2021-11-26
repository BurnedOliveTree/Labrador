from lib.Socket import Socket
import socket

class ServerSocket(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.main_socket: socket.socket = None

    def connect(self) -> None:
        if not self.socket and not self.main_socket:
            self.main_socket = socket.socket(socket.AF_INET6 if ":" in self.host else socket.AF_INET, socket.SOCK_STREAM)
            self.main_socket.bind((self.host, self.port))
            self.main_socket.listen(1)
            self.socket, self.client_adress = self.main_socket.accept()

    def disconnect(self) -> None:
        if self.socket and self.main_socket:
            self.main_socket.close()
            self.socket.close()
            self.main_socket = None
            self.socket = None