class Host:
    def __init__(self, argv: list):
        # python3 client.py [IP_VERSION_NUMBER] [PORT_NUMBER] [ADDRESS]
        self.ip_version = int(argv[1]) if len(argv) >= 2 and argv[1] in ['4', '6'] else 4
        self.host = argv[3] if len(argv) >= 4 else self.get_default_host_address(self.ip_version)
        self.port = int(argv[2]) if len(argv) >= 3 else 8000
    
    def get_default_host_address(self, ip_version: int) -> str:
        if ip_version == 4:
            return "127.0.0.1"
        elif ip_version == 6:
            return "::1"