from lib.UDP.SocketUDP import SocketUDP

class ServerSocket(SocketUDP):

    def establish_connection(self) -> None:
        super().create_UDP_socket()
        self.bind(self.socket, self.host, self.port)
    
