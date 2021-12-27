from io import BytesIO
from threading import Lock
from lib.TCP.SocketTCP import SocketTCP
from lib.RawSocket import RawSocket
from select import poll, POLLIN
import logging

class ServerSocket(SocketTCP):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.poll = poll()
        self.main_socket: RawSocket = None
        self.mutex = Lock()
        self.sockets: dict[int, RawSocket] = {}
        self.server_num_workers = 5

    def read(self):
        sockets_answer = []
        for fd, socket in [(fd, self.sockets[fd]) for fd, _ in self.poll.poll()]:
            sockets_answer.append((fd, super().read(socket=socket)))
        return sockets_answer
    
    def send(self, binary_stream: BytesIO, fd: int):
        super().send(binary_stream, socket = self.sockets[fd])

    def connect(self) -> None or bool:
        if not self.main_socket:
            self.main_socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "TCP")
            if self.main_socket.bind(self.host, self.port) == False:
                return False
            self.main_socket.listen(self.server_num_workers)
            logging.info('Server is listening...')
        accept_returns = self.main_socket.accept()
        if accept_returns == False:
            return False
        socket, _ = accept_returns
        socket.setblocking(0)
        self.poll.register(socket.fileno(), POLLIN)
        self.mutex.acquire(1)
        self.sockets[socket.fileno()] = RawSocket(created_socket = socket)
        self.mutex.release()
        logging.info('Using TCP socket')

    def disconnect(self, fd: int = None) -> None:
        if fd:
            self.poll.unregister(fd)
            self.mutex.acquire(1)
            self.sockets[fd].disconnect()
            self.sockets.pop(fd)
            self.mutex.release()
        else:
            if self.main_socket:
                self.main_socket.disconnect()
                self.main_socket = None
            if self.sockets:
                self.mutex.acquire(1)
                for fd, socket in self.sockets.items():
                    self.poll.unregister(fd)
                    socket.disconnect()
                self.sockets = {}
                self.mutex.release()
