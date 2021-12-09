from lib.SocketInterface import SocketInterface
from select import poll, POLLIN

class Poll:
    def __init__(self) -> None:
        self.poll = poll()
        self.sockets: dict[int, SocketInterface] = {}
    
    def register(self, socket: SocketInterface) -> None:
        self.poll.register(socket.socket.socket.socket.fileno(), POLLIN)
        self.sockets[socket.socket.socket.socket.fileno()] = socket
    
    def unregister(self, socket: SocketInterface) -> None:
        self.poll.unregister(socket.socket.socket.socket.fileno())
        self.sockets.pop(socket.socket.socket.socket.fileno())
    
    def read(self) -> list[SocketInterface]:
        return [self.sockets[fd] for fd, _ in self.poll.poll()]