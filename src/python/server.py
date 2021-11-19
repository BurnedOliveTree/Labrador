import sys
from lib.Socket import ServerSocketInterface
from lib.Host import Host
import logging
from pynput.keyboard import Key, Listener
import threading

class Server(Host):
    def __init__(self, argv: list):
        # python3 server.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)
        self.socket = None
    
    def on_release(self, key):
        if key == Key.esc:
            self.socket.send("QUIT")
            sys.exit()

    def listen(self) -> None:
        data = None
        with ServerSocketInterface(self.host, self.port) as self.socket:
            self.socket.bind()
            print("Listening on ", self.host, ":", self.port)
            while data not in ["", "QUIT"]:
                data, host = self.socket.read()
                print(f"Receiving data from: {host}\nReceived data: {data}")
                self.socket.send(data, host)
            else:
                if data == "":
                    print("ERROR: Received an empty datagram, exiting now...")
                elif data == 'QUIT':
                    print("Received a signal to end, exiting now...")
        
    def get_admin_command(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()
            

if __name__ == "__main__":
    logging.basicConfig(filename='../../log/server.log', encoding='utf-8', level=logging.DEBUG)
    server = Server(sys.argv)
    server_listening = threading.Thread(target=server.listen)
    server_listening.start()
    server.get_admin_command()
