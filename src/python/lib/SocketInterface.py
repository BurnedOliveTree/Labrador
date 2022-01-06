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
                decoded_data = struct.unpack('!HBB', data[1:])  # TODO this needs to not be hardcoded
            else:
                is_struct = False
                decoded_data = self.decode(data[1:])
            if ret_address:
                return decoded_data, address, is_struct
            else:
                return decoded_data
        raise ValueError('Data not received')

    def send(self, data: bytes, address: str = None, is_struct=False) -> None:
        s = bytes("0123456789ABCDEF", 'utf-8')
        type_file = 0
        status_code = 0
        id_file = 1
        encoded_data = struct.pack('!HBB16s', id_file, type_file, status_code, s) + data  # TODO this needs to not be hardcoded
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
        if data:
            return data.encode("ascii")
        return b""

    def decode(self, data: bytes) -> str:
        if data:
            return data.decode("ascii")
        return ""

    def connect(self) -> None or bool:
        self.binary_stream = io.BytesIO()
        return self.socket.connect()

    def disconnect(self) -> None:
        self.binary_stream.close()
        self.socket.disconnect()

    def __enter__(self):
        succeeded_bind = self.connect()
        if succeeded_bind == False:
            self.disconnect()
            return None
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()
