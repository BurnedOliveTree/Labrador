import socket
import sys


class Server:
    def __init__(self, argv: list):
        self.host = '127.0.0.1'
        self.buffer_size = 1024
        if len(argv) < 2:
            self.port = 8000
        else:
            self.port = int(argv[1])
        print("Listening on ", self.host, ":", self.port)

    def listen(self):
        datagram_number = 1
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as new_socket:
            new_socket.bind((self.host, self.port))
            while True:
                data, address = new_socket.recvfrom(self.buffer_size)
                print("Receiving data from: {}".format(address))
                print("Received data: {}".format(data))

                if not data:
                    print("ERROR: Received an empty datagram, exiting now...")
                    break
                new_socket.sendto(data, address)
                print('Sending datagram #', datagram_number)
                datagram_number += 1


if __name__ == "__main__":
    Server(sys.argv).listen()
