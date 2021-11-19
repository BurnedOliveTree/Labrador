import logging, signal, sys
from lib.Socket import ServerSocketInterface
from lib.Host import Host
from pynput.keyboard import Key, Listener
from threading import Thread

class Server(Host):
    def __init__(self, argv: list):
        # python3 server.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        super().__init__(argv)
        self.socket = None
        self.is_quit_sent = False
        signal.signal(signal.SIGINT, self.__on_sig_int)

    def listen(self) -> None:
        data = None
        with ServerSocketInterface(self.host, self.port) as self.socket:
            self.socket.bind()
            print("Listening on ", self.host, ":", self.port)
            while data not in ["", "QUIT"]:
                data, host, is_struct = self.socket.read()
                print(f"Receiving data from: {host}\nReceived data: {data}")
                self.socket.send(data, host, is_struct)
            else:
                self.is_quit_sent = True
                if data == "":
                    print("ERROR: Received an empty datagram, exiting now...")
                elif data == 'QUIT':
                    print("Received a signal to end, exiting now...")
    
    def __on_release(self, key):
        if key == Key.esc:
            self.socket.send("QUIT")
            return False
        return not self.is_quit_sent
    
    def __on_sig_int(self, signum, frame):
        signal.signal(signum, signal.SIG_IGN)
        self.socket.send("QUIT")
        self.is_quit_sent = True
        
    def get_admin_command(self):
        with Listener(on_release=self.__on_release) as listener:
            listener.join()
            

if __name__ == "__main__":
    logging.basicConfig(filename='../../log/server.log', encoding='utf-8', level=logging.DEBUG)
    server = Server(sys.argv)
    server_listening = Thread(target=server.listen)
    server_listening.start()
    server.get_admin_command()
