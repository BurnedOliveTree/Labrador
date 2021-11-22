
from lib.SocketInterface import SocketInterface

class ServerSocketInterface(SocketInterface):
    def read(self) -> tuple:
        return super().read(True)