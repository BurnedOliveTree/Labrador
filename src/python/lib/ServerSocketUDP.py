from lib.Socket import Socket

class ServerSocket(Socket):
    def connect(self) -> None:
        super().connect()
        self.socket.bind((self.host, self.port))
