from lib.TCP.SocketTCP import SocketTCP
import logging

from lib.RawSocket import RawSocket

class ServerSocket(SocketTCP):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.main_socket: RawSocket = None
        self.sockets: list[RawSocket] = []

    def connect(self) -> None or bool:
        if not self.sockets and not self.main_socket:
            self.main_socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "TCP")
            if self.main_socket.bind(self.host, self.port) == False:
                return False
            self.main_socket.listen(1)
            accept_returns = self.main_socket.accept()
            if accept_returns == False:
                return False
            socket, self.client_adress = accept_returns
            self.sockets.append(RawSocket(created_socket = socket))
            logging.info('Using TCP socket')

    def disconnect(self) -> None:
        if self.main_socket:
            self.main_socket.disconnect()
            self.main_socket = None
        if self.sockets:
            for socket in self.sockets:
                socket.disconnect()
            self.sockets = []