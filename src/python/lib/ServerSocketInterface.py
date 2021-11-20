
from lib.SocketInterface import SocketInterface

class ServerSocketInterface(SocketInterface):
    def __init__(self, socket):
        super().__init__(socket)
        self.socket = socket
    
    def bind(self) -> None:
        self.socket.bind()
    
    def read(self) -> tuple:
        return super().read(True)