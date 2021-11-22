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
        self.packet_size = 65536
        self.timeout = 10
    
    def read(self) -> None:
        address = None
        amount, current_amount = 1, 0
        data_map: dict = {}
        while current_amount < amount:
            try:
                datagram, address = self.socket.recvfrom(65536)
                data, size, amount, number = self.__split_read_data(datagram)
                data_map[number] = data
                current_amount += 1
            except socket.error:
                if len(data_map) > 0:
                    logging.warn("Socket timed out, data is probably corrupted")
                    current_amount += 1
                else:
                    amount, current_amount = 1, 0
        data = b''.join(val for (_, val) in data_map.items())
        return data, address
    
    def __split_read_data(self, datagram: bytes):
        header = datagram[:4]
        size = int(header[0] * (2 ** 8) + header[1])
        amount = int(header[2])
        number = int(header[3])
        return datagram[4:], size, amount, number

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self.__split_send_data(binary_stream.read())
        for datagram in data:
            self.socket.sendto(datagram, address)
            logging.debug('Sending datagram #%s: %s', datagram_number, datagram)
            datagram_number += 1
    
    def __create_datagram(self, raw_data: bytes, amount: int, number: int, data_range: tuple):
        datagram: bytearray = bytearray(b'')
        size = (data_range[1] if data_range[1] else len(raw_data)) - data_range[0]
        datagram.extend(byte(size // 256))
        datagram.extend(byte(size % 256))
        datagram.extend(byte(amount % 256))
        datagram.extend(byte(number % 256))
        datagram.extend(raw_data[data_range[0]:data_range[1]])
        return bytes(datagram)
    
    def __split_send_data(self, raw_data: bytes) -> str:
        data = []
        max_size = min(65536, self.packet_size, len(raw_data) + 4) - 4     # TODO len(raw_data) - to be deleted
        datagram_amount = len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)
        if datagram_amount >= 256:
            raise ValueError("Given data was too big, resulting in too many datagrams")
        for i in range(0, datagram_amount - 1):
            data.append(self.__create_datagram(raw_data, datagram_amount, i, (max_size * i, max_size * (i + 1))))
        data.append(self.__create_datagram(raw_data, datagram_amount, datagram_amount - 1, (-(len(raw_data) % max_size), None)))
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
