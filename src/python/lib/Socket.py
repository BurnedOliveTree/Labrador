import io, logging, socket
from numpy import byte

# Datagram structure:
# D - data, A - amount of all datagrams for this data, F - flags, N - number of datagram
# AAAAAAAA
# AAAAAAAA
# FNNNNNNN
# NNNNNNNN
# DDDDD...
class Socket:
    def __init__(self, host: str, port: str):
        self.socket: socket.socket = None
        self.host: str = host
        self.port: str = port
        self.buffer_size = 32
        self.timeout = 10
    
    def read(self) -> None:
        address = None
        size, current_size = 1, 0
        data_map: dict = {}
        while current_size < size:
            try:
                datagram, address = self.socket.recvfrom(self.buffer_size)
                data, size, _, number = self.__split_read_data(datagram)
                data_map[number] = data
                current_size += 1
            except socket.error:
                if len(data_map) > 0:
                    logging.warn("Socket timed out, data is probably corrupted")
                    current_size += 1
                else:
                    size, current_size = 1, 0
        data = b''.join(val for (_, val) in data_map.items())
        return data, address
    
    def __split_read_data(self, datagram: bytes):
        header = datagram[:4]
        size = int(header[0] * (2 ** 8) + header[1])
        is_complex = bool(header[2] << 7)
        number = int((header[2] & 0x7F) * (2 ** 8) + header[3])
        return datagram[4:], size, is_complex, number

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self.__split_send_data(binary_stream.read())
        for datagram in data:
            self.socket.sendto(datagram, address)
            logging.debug('Sending datagram #%s: %s', datagram_number, datagram)
            datagram_number += 1
    
    def __create_datagram(self, raw_data, amount, number, data_range: tuple, flag = 0x80):
        datagram: bytearray = bytearray(b'')
        datagram.extend([ byte(amount // 256), byte(amount % 256) ])
        datagram.extend([ byte(flag | (number // 256)), byte(number % 256) ])
        datagram.extend(raw_data[data_range[0]:data_range[1]])
        return bytes(datagram)
    
    def __split_send_data(self, raw_data: bytes) -> str:
        if self.buffer_size >= 65536:
            raise ValueError("Given buffer size is too big")
        max_size = self.buffer_size - 4
        data = []
        datagram_amount = len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)
        for i in range(0, len(raw_data) - max_size, max_size):
            data.append(self.__create_datagram(raw_data, datagram_amount, i, (i, i + max_size)))
        data.append(self.__create_datagram(raw_data, datagram_amount, len(data), (-(len(raw_data) % max_size), None), 0x7F))
        if len(data) >= 32768:
            raise ValueError("Given data was too big, resulting in too many datagrams")
        return data
    
    def connect(self) -> None:
        if not self.socket:
            self.socket = socket.socket(socket.AF_INET6 if ":" in self.host else socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()
