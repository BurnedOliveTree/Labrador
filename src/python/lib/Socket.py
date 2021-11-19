import socket, io
from numpy import byte

# Datagram structure:
# D - data, S - size, F - flags, N - number of datagram
# SSSSSSSS
# SSSSSSSS
# FNNNNNNN
# DDDDDDDD
# DDDDD...
class Socket:
    def __init__(self, host: str, port: str):
        self.socket: socket.socket = None
        self.host: str = host
        self.port: str = port
        self.buffer_size = 32
    
    def read(self) -> None:
        size, current_size = 1, 0
        data_map: dict = {}
        while current_size < size:
            datagram, address = self.socket.recvfrom(self.buffer_size)
            data, size, _, number = self.__split_read_data(datagram)
            data_map[number] = data
            current_size += 1
        data = b''.join(val for (_, val) in data_map.items())
        return data, address
    
    def __split_read_data(self, datagram):
        header = datagram[:3]
        size = int(header[0] * (2 ** 8) + header[1])
        is_complex = bool(header[2] << 7)
        number = int(header[2] << 1)
        return datagram[3:], size, is_complex, number

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self.__split_send_data(binary_stream.read())
        for datagram in data:
            self.socket.sendto(datagram, address)
            print('Sending datagram #', datagram_number, ": ", datagram)    # TODO this needs to go
            datagram_number += 1
    
    def __split_send_data(self, raw_data: bytes) -> str:
        if self.buffer_size >= 65536:
            raise Exception("Buffer size is to big")                        # TODO specify exception type
        max_size = self.buffer_size - 3
        data = []
        for i in range(0, len(raw_data) - max_size, max_size):
            datagram: bytearray = bytearray(b'')
            if len(raw_data) // self.buffer_size <= 256:
                datagram.extend(byte(0))
            datagram.extend(byte(len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)))  # TODO this should be two bytes, but is one, so it will break for bigger messages
            datagram.extend(byte(0x80 | i))
            datagram.extend(raw_data[i:i+max_size])
            data.append(bytes(datagram))
        datagram: bytearray = bytearray(b'')
        if len(raw_data) // self.buffer_size <= 256:
            datagram.extend(byte(0x00))
        datagram.extend(byte(len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)))  # TODO this should be two bytes, but is one, so it will break for bigger messages
        if len(data) == 0:
            datagram.extend(byte(0x7F | len(data)))
        else:
            datagram.extend(byte(0x80 | len(data)))
        datagram.extend(raw_data[-(len(raw_data) % max_size):])
        data.append(bytes(datagram))
        if len(data) >= 128:
            raise Exception("Too many packets")                             # TODO specify exception type
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