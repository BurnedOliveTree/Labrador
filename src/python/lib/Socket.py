import io, logging, struct

from lib.RawSocket import RawSocket

class Socket:
    def __init__(self, host: str, port: str):
        self.socket: RawSocket = None
        self.host: str = host
        self.port: str = port
        self.packet_size = 7
        self.client_adress = None
        self.header_types = '!HBB'  

    def read(self):
        raise NotImplementedError("This method is an interface and shouldn't be called directly")
    
    def _split_read_data(self, datagram: bytes):
        header = datagram[:struct.calcsize(self.header_types)]
        size, amount, number = struct.unpack(self.header_types, header)
        return datagram[struct.calcsize(self.header_types):], size, amount, number

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        if address is None:
            address = (self.host, self.port)
        data = self._split_send_data(binary_stream.read(), self.socket.buffer_size)
        for datagram in data:
            self.socket.sendto(datagram, address)
            logging.debug('Sending datagram #%s: %s', datagram_number, datagram)
            datagram_number += 1
    
    def __create_datagram(self, raw_data: bytes, amount: int, number: int, data_range: tuple):
        datagram: bytearray = bytearray(b'')
        size = (data_range[1] if data_range[1] else len(raw_data)) - data_range[0]
        datagram.extend(struct.pack(self.header_types, size, amount, number))
        datagram.extend(raw_data[data_range[0]:data_range[1]])
        return bytes(datagram)
    
    def _split_send_data(self, raw_data: bytes, buffer_size: int) -> str:
        data = []
        max_size = min(buffer_size + 1, self.packet_size) - struct.calcsize(self.header_types)
        datagram_amount = len(raw_data) // max_size + (1 if len(raw_data) % max_size != 0 else 0)
        if datagram_amount >= 256 ** struct.calcsize(self.header_types[2]):
            raise ValueError("Given data was too big, resulting in too many datagrams")
        for i in range(0, datagram_amount - 1):
            data.append(self.__create_datagram(raw_data, datagram_amount, i, (max_size * i, max_size * (i + 1))))
        data.append(self.__create_datagram(raw_data, datagram_amount, datagram_amount - 1, ((datagram_amount - 1) * max_size, None)))
        return data
    
    def connect(self):
        raise NotImplementedError("This method is an interface and shouldn't be called directly")
    
    def disconnect(self):
        if self.socket:
            self.socket.disconnect()

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()