import io, logging, socket, struct

class Socket:
    def __init__(self, host: str, port: str):
        self.socket: socket.socket = None
        self.host: str = host
        self.port: str = port
        self.packet_size = 256
        self.client_adress = None
        self.header_types = '!IHH'
    
    def read(self):
        address = None
        amount, current_amount = 1, 0
        data_map: dict = {}
        while current_amount < amount:
            try:
                datagram, address = self.socket.recvfrom(65536)
                if address is not None:
                    self.client_adress = address
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
        return data, self.client_adress
    
    def __split_read_data(self, datagram: bytes):
        header = datagram[:struct.calcsize(self.header_types)]
        size, amount, number = struct.unpack(self.header_types, header)
        return datagram[struct.calcsize(self.header_types):], size, amount, number

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
        datagram.extend(struct.pack(self.header_types, size, amount, number))
        datagram.extend(raw_data[data_range[0]:data_range[1]])
        return bytes(datagram)
    
    def __split_send_data(self, raw_data: bytes) -> str:
        data = []
        max_size = min(65536, self.packet_size) - struct.calcsize(self.header_types)
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

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()
