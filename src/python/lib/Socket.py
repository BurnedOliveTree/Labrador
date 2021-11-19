import socket, io

class Socket:
    def __init__(self, host: str, port: str):
        self.socket: socket.socket = None
        self.host: str = host
        self.port: str = port
        self.buffer_size = 32
    
    def read(self) -> None:
        return self.socket.recvfrom(self.buffer_size)

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self.__split_data(binary_stream.read())
        for datagram in data:
            self.socket.sendto(datagram, address)
            print('Sending datagram #', datagram_number, ": ", datagram)    # TODO this needs to go
            datagram_number += 1
    
    def __split_data(self, raw_data: bytes) -> str:
        data = [ raw_data[i:i+self.buffer_size] for i in range(0, len(raw_data) - self.buffer_size, self.buffer_size) ]
        data.append(raw_data[-(len(raw_data) % self.buffer_size):])
        return data
    
    def connect(self) -> None:
        self.socket = socket.socket(socket.AF_INET6 if ":" in self.host else socket.AF_INET, socket.SOCK_DGRAM)

    def disconnect(self) -> None:
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()


class SocketInterface:
    def __init__(self, host: str, port: str):
        self.binary_stream = None
        self.socket = Socket(host, port)  # TODO do not construct here
    
    def read(self, ret_address: bool = False) -> str or tuple:
        data, address = self.socket.read()
        if ret_address:
            return self.decode(data), address
        else:
            return self.decode(data)

    def send(self, data: str, address: str = None) -> None:
        encoded_data = self.encode(data)
        self.__write_to_binary_stream(encoded_data)
        self.socket.send(self.binary_stream, address)
        self.__clear_binary_stream()
    
    def __clear_binary_stream(self) -> None:
        self.binary_stream.seek(0)
        self.binary_stream.truncate(0)
    
    def __write_to_binary_stream(self, data: bytes) -> None:
        self.binary_stream.write(data)
        self.binary_stream.seek(0)

    def encode(self, data: str) -> bytes:
        return data.encode("ascii")

    def decode(self, data: bytes) -> str:
        return data.decode("ascii")

    def connect(self) -> None:
        self.binary_stream = io.BytesIO()
        self.socket.connect()

    def disconnect(self) -> None:
        self.binary_stream.close()
        self.socket.disconnect()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()


class ServerSocket(Socket):
    def bind(self) -> None:
        self.socket.bind((self.host, self.port))


class ServerSocketInterface(SocketInterface):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket = ServerSocket(host, port)  # TODO do not construct here
    
    def bind(self) -> None:
        self.socket.bind()
    
    def read(self) -> tuple:
        return super().read(True)