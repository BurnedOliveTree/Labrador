from lib.TCP.SocketTCP import SocketTCP
import logging

from lib.RawSocket import RawSocket

class ServerSocket(SocketTCP):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.main_socket: RawSocket = None

    def connect(self) -> None or bool:
        if not self.socket and not self.main_socket:
            self.main_socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "TCP")
            bind_succeed = self.main_socket.bind(self.host, self.port)
            if bind_succeed is False:
                return bind_succeed
            self.main_socket.listen(1)
            socket, self.client_adress = self.main_socket.accept()
            self.socket = RawSocket(created_socket = socket)
            logging.info('Using TCP socket')

    def disconnect(self) -> None:
        if self.main_socket:
            self.main_socket.disconnect()
        if self.socket:
            self.socket.disconnect()
            self.main_socket = None
            self.socket = None
