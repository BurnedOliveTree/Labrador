import sys
from lib.Socket import SocketInterface
from lib.Host import Host
import logging

class Client(Host):
    def __init__(self, argv: list):
        # python3 client.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)

    def connect(self) -> None:
        with SocketInterface(self.host, self.port) as socket:
            print("Will send data to ", self.host, ":", self.port)
            data = self.get_user_data()
            while data != "QUIT":
                socket.send(data, is_struct=True)           # TODO this needs to not be hardcoded
                received_data = socket.read()
                print('Received data: ', repr(received_data))
                data = self.get_user_data()
            else:
                socket.send(data)
        print('Client finished')

    def get_user_data(self) -> str:
        return input("Data: ")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='../../log/client.log', encoding='utf-8', level=logging.DEBUG)
    Client(sys.argv).connect()
