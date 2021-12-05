from lib.Socket import Socket
from struct import calcsize
import io, logging

class SocketTCP(Socket):
    def read(self):
        amount, current_amount = 1, 0
        data_map: dict = {}
        while current_amount < amount:
            header = self.socket.receive(calcsize(self.header_types))
            if header is False:
                if len(data_map) > 0:
                    current_amount += 1
                else:
                    amount, current_amount = 1, 0
                continue
            _, size, amount, number = self.split_read_data(header)
            data = self.socket.receive(size)
            data_map[number] = data
            current_amount += 1
        data = b''.join(val for (_, val) in data_map.items())
        return data, None

    def send(self, binary_stream: io.BytesIO, address: str = None) -> None:
        datagram_number = 0
        data = self.split_send_data(binary_stream.read())
        for datagram in data:
            self.socket.send(datagram)
            logging.debug('Sending datagram #%s: %s', datagram_number, datagram)
            datagram_number += 1
