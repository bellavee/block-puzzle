import socket


class Network:
    """
    Object handling connection and communication between the client and the server.
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"  # A changer
        self.port = 5000
        self.addr = (self.server, self.port)

    def connect(self):
        """
        connect() method try to connect the socket to the server.
        """
        try:
            self.client.connect(self.addr)
        except:
            print("Connection au serveur échoué")
            raise ConnectionRefusedError

    def send(self, data):
        """
        send() sends string data to the server.
        @param data:
        @return:
        """
        try:
            self.client.send(data.encode("Utf-8"))
            return self.client.recv(4096)
        except socket.error as e:
            print(e)
