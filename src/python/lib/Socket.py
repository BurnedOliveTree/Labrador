import io, logging, socket
from numpy import byte
import struct

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
            logging.debug('Sending datagram #%s: %s', datagram_number, datagram)
            datagram_number += 1
    
    def __create_datagram(self, raw_data, max_size, number, data_range: tuple, flag = 0x80):
        datagram: bytearray = bytearray(b'')
        foo = len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)
        foo = [ byte(foo // 256), byte(foo % 256) ]
        datagram.extend(foo)
        datagram.extend(byte(flag | number))
        datagram.extend(raw_data[data_range[0]:data_range[1]])
        return bytes(datagram)
    
    def __split_send_data(self, raw_data: bytes) -> str:
        if self.buffer_size >= 65536:
            raise ValueError("Given buffer size is too big")
        max_size = self.buffer_size - 3
        data = []
        for i in range(0, len(raw_data) - max_size, max_size):
            data.append(self.__create_datagram(raw_data, max_size, i, (i, i + max_size)))
        data.append(self.__create_datagram(raw_data, max_size, len(data), (-(len(raw_data) % max_size), None), 0x7F))
        if len(data) >= 128:
            raise ValueError("Given data was too big, resulting in too many datagrams")
        return data
    
    def connect(self) -> None:
        if not self.socket:
            self.socket = socket.socket(socket.AF_INET6 if ":" in self.host else socket.AF_INET, socket.SOCK_DGRAM)

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None
    
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
        if data[0] == 1:
            is_struct = True
            decoded_data = struct.unpack('hhl', data[1:])       # TODO this needs to not be hardcoded
        else:
            is_struct = False
            decoded_data = self.decode(data[1:])
        if ret_address:
            return decoded_data, address, is_struct
        else:
            return decoded_data

    def send(self, data: str, address: str = None, is_struct = False) -> None:
        if is_struct:
            encoded_data = b'\1' + struct.pack('hhl', 1, 2, 3)  # TODO this needs to not be hardcoded
        else:
            encoded_data = b'\0' + self.encode(data)
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