import logging, signal, sys
from lib.ServerSocketInterface import ServerSocketInterface
from lib.TCP.ServerSocketTCP import ServerSocket as SocketTCP
from lib.UDP.ServerSocketUDP import ServerSocket as SocketUDP
from lib.Host import Host, get_project_root
from pynput.keyboard import Key, Listener
from threading import Thread

class Server(Host):
    def __init__(self, argv: list):
        super().__init__(argv)
        self.socket = None
        self.is_quit_sent = False
        signal.signal(signal.SIGINT, self.__on_sig_int)

    def listen(self) -> None:
        data = None
        print("Listening on ", self.host, ":", self.port)
        socket = self.__get_socket()
        with ServerSocketInterface(socket) as self.socket:
            while not self.is_quit_sent:
                data, host, is_struct = self.socket.read()
                print(f"Receiving data from: {host}\nReceived data: {data}")
                self.socket.send(data, host, is_struct)
                if data == 'QUIT':
                    self.is_quit_sent = True
            else:
                print("Received a signal to end, exiting now...")
        self.socket = None
    
    def __get_socket(self):
        if self.protocol == 'UDP':
            return SocketUDP(self.host, self.port)
        elif self.protocol == 'TCP':
            return SocketTCP(self.host, self.port)
        else:
            raise ValueError(f'invalid protocol type: {self.protocol} please choose from UDP or TCP')
    
    def __on_release(self, key):
        if key == Key.esc:
            if self.socket:
                self.socket.send("QUIT")
            self.is_quit_sent = True
        return not self.is_quit_sent
    
    def __on_sig_int(self, signum, frame):
        signal.signal(signum, signal.SIG_IGN)
        self.socket.send("QUIT")
        self.is_quit_sent = True
        
    def get_admin_command(self):
        with Listener(on_release=self.__on_release) as listener:
            listener.join()
            

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=get_project_root()+'/log/server.log',
        level=logging.DEBUG
    )
    server = Server(sys.argv)
    server_listening = Thread(target=server.listen)
    server_listening.start()
    server.get_admin_command()
