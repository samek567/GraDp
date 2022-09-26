import socket
import json

class Network:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip,self.port))

    def send_data(self,data):
        '''
        To jest funkcja przyjmujaca slownik, i wysylajaca go.
        '''

        data_convert = json.dumps(data).encode("ascii")

        self.conn.send(("0" * (5 - len(str(len(data_convert)))) + str(len(data_convert))).encode("ascii"))
        self.conn.send(data_convert)

    def get_data(self):
        '''
        Jest to funkcja która pobiera dane i zwraca słownik.
        '''
        get_len = int(self.conn.recv(5).decode("ascii"))
        return json.loads(self.conn.recv(get_len).decode("ascii"))