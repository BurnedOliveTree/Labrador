import io
import socket
import sys

#TODO message > buffer size handle
#TODO clear buffer after sending message
class Client:
    def __init__(self, argv: list):
        # python3 client.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        ip_version = int(argv[1]) if len(argv) >= 2 and argv[1] in ['4', '6'] else 4
        host = argv[3] if len(argv) >= 4 else self.get_default_host_address(ip_version)
        port = int(argv[2]) if len(argv) >= 3 else 8000

        print("Will send data to ", host, ":", port)
        self.socket_interface = SocketInterface(host, port, ip_version)

    def connect(self):
        data = self.get_user_data()
        while (data.upper() != "QUIT"):
            self.socket_interface.send(data)
            recived_data = self.socket_interface.read()
            print('Received data: ', repr(recived_data))
            data = self.get_user_data()
        else:
            self.socket_interface.send(data)
            self.socket_interface.end_session()

        print('Client finished')

    def get_user_data(self):
        return input("Data: ")

    def get_default_host_address(self, ip_version):
        if ip_version == 4:
            return "127.0.0.1"
        elif ip_version == 6:
            return "::1"


        

class Socket:
    def __init__(self, host, port, ip_version):
        self.socket = socket.socket(socket.AF_INET if ip_version == 4 else socket.AF_INET6, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.buffer_size = 1024
    
    def read(self):
        return self.socket.recv(self.buffer_size)

    def send(self, binary_stream):
        self.socket.sendto(binary_stream.read(), (self.host, self.port))

    def end_session(self):
        self.socket.close()


class SocketInterface(Socket):
    def __init__(self, host, port, ip_version):
        super().__init__(host, port, ip_version)
        self.binary_stream = io.BytesIO()

    def read(self):
        data = super().read()
        return self.__decode(data)

    def send(self, data):
        data = self.__encode(data)
        self.__write_to_binary_stream(data)
        super().send(self.binary_stream)
        self.__clear_binary_stream()
    
    def __clear_binary_stream(self):
        self.binary_stream.flush()
        self.binary_stream.seek(0)
    
    def __write_to_binary_stream(self, data):
        self.binary_stream.write(data)
        self.binary_stream.seek(0)

    def __encode(self, data):
        return data.encode("ascii")

    def __decode(self, data):
        return data.decode("ascii")
    
    def end_session(self):
        self.binary_stream.close()
        super().end_session()


if __name__ == "__main__":
    Client(sys.argv).connect()
