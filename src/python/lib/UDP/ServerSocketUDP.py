from lib.UDP.SocketUDP import SocketUDP

class ServerSocket(SocketUDP):
    def connect(self) -> None:
        super().connect()
        self.socket.bind((self.host, self.port))
