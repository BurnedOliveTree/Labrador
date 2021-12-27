from lib.Socket import Socket
import logging

from lib.RawSocket import RawSocket

class SocketUDP(Socket):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
    
    def read(self):
        address = None
        amount, current_amount = 1, 0
        data_map: dict = {}
        while current_amount < amount:
            received_data = self.socket.receive_from()
            if received_data is False or received_data is None:
                if len(data_map) > 0:
                    current_amount += 1
                else:
                    amount, current_amount = 1, 0
                continue
            else:
                (datagram, address) = received_data
            if address is not None:
                self.client_adress = address
            data, _, amount, number = self._split_read_data(datagram)
            data_map[number] = data
            current_amount += 1
        data = b''.join(val for (_, val) in data_map.items())
        return data, self.client_adress

    def connect(self) -> None:
        if not self.socket:
            self.socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "UDP")
            logging.info('Using UDP socket')