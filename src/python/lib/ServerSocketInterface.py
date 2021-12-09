from lib.SocketInterface import SocketInterface

class ServerSocketInterface(SocketInterface):
    def read(self):
        sockets_answer = []
        for socket in self.sockets:
            sockets_answer.append(super().read(True, socket=socket))
        return sockets_answer
    
    def send(self):
        for socket in self.sockets:
            super().send(True, socket=socket)
        