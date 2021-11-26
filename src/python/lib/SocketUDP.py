from lib.Socket import Socket

class SocketUDP(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.timeout = 10
    
    def connect(self) -> None:
        super().__init__()    
        self.socket.settimeout(self.timeout)
