from lib.Socket import Socket

class ClientSocket(Socket):
    def connect(self) -> None:
        super().connect()
        self.socket.connect((self.host, self.port))