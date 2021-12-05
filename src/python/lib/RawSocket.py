import socket, logging

class RawSocket:
    def __init__(self, ip_version = None, protocol = None, created_socket = None):
        self.buffer_size = 65535 
        self.socket: socket.socket
        self.default_timeout = 10
        if created_socket is not None: 
            self.socket = created_socket
        elif ip_version is not None and protocol is not None:
            self.create_socket(ip_version, protocol)
    
    def receive_from(self):
        try:
            self.socket.recvfrom(self.buffer_size)
        except socket.error as err:
            logging.warn(f"Socket timed out, data is probably corrupted. Message: {err}")
            return False
    
    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def connect(self, host, port):
        if self.socket:
            self.socket.connect((host, port))
    
    def enable_timeout(self):
        self.socket.settimeout(self.default_timeout)
    
    def create_socket(self, ip_version, protocol):
        if (ip_version == 'ipv4' and protocol == 'TCP'):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif (ip_version == 'ipv6' and protocol == 'TCP'):
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        elif (ip_version == 'ipv4' and protocol == 'UDP'):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif (ip_version == 'ipv6' and protocol == 'TCP'):
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        
    def bind(self, host, port):
        try:
            self.socket.bind((host, port))
        except socket.error as message:
            logging.critical(f"Bind failed. Message {message}")
            return False
    
    def listen(self, num_workers):
        return self.socket.listen(num_workers)
    
    def accept(self):
        return self.socket.accept()
    
    def receive(self, size):
        return self.socket.recv(size)
    
    def send(self, datagram):
       return self.socket.send(datagram)
    
    def sendto(self, datagram, address):
        return self.socket.sendto(datagram, address)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()