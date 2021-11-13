import sys
from Socket import ServerSocketInterface
from Host import Host

class Server(Host):
    def __init__(self, argv: list):
        # python3 server.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)
        self.socket_interface = ServerSocketInterface(self.host, self.port, self.ip_version)
        print("Listening on ", self.host, ":", self.port)

    def listen(self):
        data = None
        self.socket_interface.bind()
        while data not in ["", "QUIT"]:
            data, host = self.socket_interface.read()
            print(f"Receiving data from: {host}\nReceived data: {data}")
            self.socket_interface.send(data, host)
        else:
            if data == "":
                print("ERROR: Received an empty datagram, exiting now...")
            elif data == 'QUIT':
                print("Received a signal to end, exiting now...")
            self.socket_interface.end_session()


if __name__ == "__main__":
    Server(sys.argv).listen()
