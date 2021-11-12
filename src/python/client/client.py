import io
import socket
import sys


class Client:
    def __init__(self, argv: list):
        # python3 client.py [PORT_NUMBER] [IP_VERSION_NUMBER]
        if len(argv) < 3 or int(argv[2]) != 6:
            self.ip_version = 4
            self.host = '127.0.0.1'
        else:
            self.ip_version = 6
            self.host = '::1'
        self.buffer_size = 1024
        if len(argv) < 2:
            self.port = 8000
        else:
            self.port = int(argv[1])
        print("Will send data to ", self.host, ":", self.port)

    def send(self):
        binary_stream = io.BytesIO()
        with socket.socket(socket.AF_INET if self.ip_version == 4 else socket.AF_INET6, socket.SOCK_DGRAM) as new_socket:
            binary_stream.write("Hello, world!\n".encode('ascii'))
            binary_stream.seek(0)
            new_socket.sendto(binary_stream.read(), (self.host, self.port))
            print('Send data to server')
            data = new_socket.recv(self.buffer_size)
            print('Received data: ', repr(data), " of size: ", self.buffer_size)
        binary_stream.close()
        print('Client finished')


if __name__ == "__main__":
    Client(sys.argv).send()
