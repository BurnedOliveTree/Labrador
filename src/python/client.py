import sys
from Socket import SocketInterface
from Host import Host

#TODO message > buffer size handle
class Client(Host):
    def __init__(self, argv: list):
        # python3 client.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)

        print("Will send data to ", self.host, ":", self.port)
        self.socket_interface = SocketInterface(self.host, self.port, self.ip_version)

    def connect(self):
        data = self.get_user_data()
        while (data != "QUIT"):
            self.socket_interface.send(data)
            recived_data = self.socket_interface.read()
            print('Received data: ', repr(recived_data))
            data = self.get_user_data()
        else:
            self.socket_interface.send(data)
            self.socket_interface.end_session()

        print('Client finished')

    def get_user_data(self):
        return input("Data: ")


if __name__ == "__main__":
    Client(sys.argv).connect()
