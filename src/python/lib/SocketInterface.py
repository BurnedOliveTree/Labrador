import struct, io

class SocketInterface:
    def __init__(self, socket):
        self.binary_stream = None
        self.socket = socket
    
    def read(self, ret_address: bool = False) -> str or tuple:
        data, address = self.socket.read()
        if data:
            if data[0] == 1:
                is_struct = True
                decoded_data = struct.unpack('!iil', data[1:])  # TODO this needs to not be hardcoded
            else:
                is_struct = False
                decoded_data = self.decode(data[1:])
            if ret_address:
                return decoded_data, address, is_struct
            else:
                return decoded_data
        raise ValueError('Data not received')

    def send(self, data: str, address: str = None, is_struct = False) -> None:
        if is_struct:
            encoded_data = b'\1' + struct.pack('!iil', 1, 2, 3)  # TODO this needs to not be hardcoded
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

