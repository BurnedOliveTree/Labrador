from lib.Socket import Socket

class ServerSocket(Socket):
    def bind(self) -> None:
        self.socket.bind((self.host, self.port))