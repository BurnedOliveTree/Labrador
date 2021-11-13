import socket
import io

END_OF_DATA = b'\x00'


class Socket:
    def __init__(self, host, port, ip_version):
        self.socket = socket.socket(socket.AF_INET if ip_version == 4 else socket.AF_INET6, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.buffer_size = 1024
    
    def read(self):
        return self.socket.recv(self.buffer_size)

    def send(self, binary_stream: io.BytesIO, address=None):
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self.__split_data(binary_stream.read())
        for datagram in data:
            self.socket.sendto(datagram, address)
            print('Sending datagram #', datagram_number, ": ", datagram)
            datagram_number += 1
    
    def __split_data(self, raw_data):
        data = [ raw_data[i:i+self.buffer_size] for i in range(0, len(raw_data) - self.buffer_size, self.buffer_size) ]
        data.append(raw_data[-(self.buffer_size - (len(raw_data) % self.buffer_size)):])
        data.append(END_OF_DATA)
        return data

    def end_session(self):
        self.socket.close()


class SocketInterface:
    def __init__(self, host, port, ip_version):
        self.binary_stream = io.BytesIO()
        self.socket = Socket(host, port, ip_version)
    
    def read(self):
        datagram = self.socket.read()
        data = datagram
        while datagram != END_OF_DATA:
            datagram = self.socket.read()
            data = data + datagram
        else:
            data = data.strip(END_OF_DATA)
        return self.decode(data)

    def send(self, data, address=None):
        data = self.encode(data)
        self.__write_to_binary_stream(data)
        self.socket.send(self.binary_stream, address)
        self.__clear_binary_stream()
    
    def __clear_binary_stream(self):
        self.binary_stream.seek(0)
        self.binary_stream.truncate(0)
    
    def __write_to_binary_stream(self, data):
        self.binary_stream.write(data)
        self.binary_stream.seek(0)

    def encode(self, data):
        return data.encode("ascii")

    def decode(self, data):
        return data.decode("ascii")
    
    def end_session(self):
        self.binary_stream.close()
        self.socket.end_session()


class ServerSocket(Socket):
    def bind(self):
        self.socket.bind((self.host, self.port))
    
    def read(self):
        return self.socket.recvfrom(self.buffer_size)


class ServerSocketInterface(SocketInterface):
    def __init__(self, host, port, ip_version):
        super().__init__(host, port, ip_version)
        self.socket = ServerSocket(host, port, ip_version)
    
    def bind(self):
        self.socket.bind()
    
    def read(self):
        datagram, address = self.socket.read()
        data = datagram
        while datagram != END_OF_DATA:
            datagram, address = self.socket.read()
            data = data + datagram
        else:
            data = data.strip(END_OF_DATA)
        return self.decode(data), address