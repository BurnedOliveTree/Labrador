from struct import pack, unpack
from lib.ServerSocketInterface import ServerSocketInterface

class ServerSocketInterfaceTCP(ServerSocketInterface):
    def read(self, ret_address: bool = True) -> str or tuple:
        result = []
        for id, answer in self.socket.read():
            data, address = answer
            if data:
                if data[0] == 1:
                    is_struct = True
                    decoded_data = unpack('!HBB', data[1:])  # TODO this needs to not be hardcoded
                else:
                    is_struct = False
                    decoded_data = self.decode(data[1:])
                if ret_address:
                    result.append((decoded_data, id, is_struct))
                else:
                    result.append(decoded_data)
            else:
                raise ValueError('Data not received')
        return result
    
    def send(self, data: str, id: int, is_struct = False) -> None:
        if is_struct:
            encoded_data = b'\1' + pack('!HBB', 1, 2, 3)  # TODO this needs to not be hardcoded
        else:
            encoded_data = b'\0' + self.encode(data)
        self.write_to_binary_stream(encoded_data)
        self.socket.send(self.binary_stream, id)
        self.clear_binary_stream()