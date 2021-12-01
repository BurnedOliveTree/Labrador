from lib.Socket import Socket
from struct import calcsize

class SocketTCP(Socket):
    def read(self):
        address = None
        amount, current_amount = 1, 0
        data_map: dict = {}
        while current_amount < amount:
            header, address = self.socket.recvfrom(calcsize(self.header_types))
            if address is not None:
                self.client_adress = address
            _, size, amount, number = self.split_read_data(header)
            data, address = self.socket.recvfrom(size)
            data_map[number] = data
            current_amount += 1
        data = b''.join(val for (_, val) in data_map.items())
        return data, self.client_adress
