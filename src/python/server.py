import sys
from lib.Socket import ServerSocketInterface
from lib.Host import Host

class Server(Host):
    def __init__(self, argv: list):
        # python3 server.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)

    def listen(self) -> None:
        data = None
        with ServerSocketInterface(self.host, self.port) as socket:
            socket.bind()
            print("Listening on ", self.host, ":", self.port)
            while data not in ["", "QUIT"]:
                data, host = socket.read()
                print(f"Receiving data from: {host}\nReceived data: {data}")
                socket.send(data, host)
            else:
                if data == "":
                    print("ERROR: Received an empty datagram, exiting now...")
                elif data == 'QUIT':
                    print("Received a signal to end, exiting now...")
                socket.disconnect()


if __name__ == "__main__":
    Server(sys.argv).listen()
