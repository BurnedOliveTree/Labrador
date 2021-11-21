import sys
from lib.SocketInterface import SocketInterface
from lib.Socket import Socket
from lib.Host import Host, get_project_root
import logging

class Client(Host):
    def __init__(self, argv: list):
        # python3 client.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)
        self.send_type_is_struct = False

    def connect(self) -> None:
        self.get_input_type()
        socket = Socket(self.host, self.port)
        received_data = None
        with SocketInterface(socket) as socket:
            print("Will send data to ", self.host, ":", self.port)
            data = self.get_user_data()
            while data != "QUIT":
                socket.send(data, is_struct=self.send_type_is_struct)
                received_data = socket.read()
                print('Received data: ', repr(received_data))
                data = self.get_user_data()
            else:
                socket.send(data)
        print('Client finished')

    def get_user_data(self) -> str:
        if self.send_type_is_struct:
            return input("Press Enter to send struct ort type 'QUIT': ")
        return input("Data: ")
    
    def get_input_type(self) -> bool:
        input_type = input("Choose type of sending data: \n 1.string\n 2.struct\nChoise: ")
        try:
            option = int(input_type)
            if option == 2:
                self.send_type_is_struct = True
        except ValueError:
            print("Wrong input! Sending default input type - string")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=get_project_root()+'/log/client.log',
        level=logging.DEBUG
    )
    Client(sys.argv).connect()
