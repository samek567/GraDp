from os import access
import socket
import json

class Network:
    def __init__(self,game_board):
        self.ip = "0.0.0.0"
        self.port = 8500
        self.number_connection = 10
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.number_connection)
        self.game_board = game_board

        self.connections = {}

    def keep_accepting(self):
        while True:
            self.accept_connection()


    def accept_connection(self):
        '''
        Jest to funkcja która przyjmuje połączenie i sprawdza czy nick jest poprawny (nie ma go w grze) i zwraca True
        jesli wszystko jest OK a false jesli nie.
        '''
        conn, adress = self.server.accept()
        get_len = int(conn.recv(5).decode("ascii"))
        nick = json.loads(conn.recv(get_len).decode("ascii"))['nick']
         
        if nick in self.connections.keys():
            conn.close()
            print("Odrzucone Polaczenie!!!")
            return False
        else:
            self.game_board.add_player(nick)
            self.connections[nick] = (conn,adress)
            self.send_data({"Wiadomosc": "Jest OK wchodzisz do gry"},nick)

            self.send_data(self.game_board.convert_to_dict(True),nick)

            return True

        print(nick)

    def send_data(self,data,nick):
        '''
        To jest funkcja przyjmujaca slownik, i wysylajaca go do gracza o podanym nicku.
        '''

        data_convert = json.dumps(data).encode("ascii")

        self.connections[nick][0].send(("0" * (5 - len(str(len(data_convert)))) + str(len(data_convert))).encode("ascii"))
        self.connections[nick][0].send(data_convert)

    def delete_connection(self,nick):
        self.connections.pop(nick)
        self.game_board.delete_player(nick)
        print(f"Usuwamy gracza o nicku: {nick}")

    def send_to_everyone(self,data):
        '''
        To jest funkcja wysyłająca dane do każdego gracza.
        '''
        out_player = []
        data_convert = json.dumps(data).encode("ascii")
        for key,value in self.connections.items():
            try:
                value[0].send(("0" * (5 - len(str(len(data_convert)))) + str(len(data_convert))).encode("ascii"))
                value[0].send(data_convert)
            except ConnectionAbortedError:
                # Jesli polaczenie zostalo zerwane(gracz wyszedl z gry) to usuwamy go z listy graczy na serwerze.
                out_player.append(key)
                

        for key in out_player:
            self.delete_connection(key)


    def get_data(self,nick):
        '''
        Jest to funkcja która pobiera dane od gracza o podanym nicku i zwraca słownik.
        '''
        get_len = int(self.connections[nick][0].recv(5).decode("ascii"))
        return json.loads(self.connections[nick][0].recv(get_len).decode("ascii"))

    def get_from_everyone(self):
        '''
        To jest funkcja zwracająca słownik, którego kluczami są nicki a wartościami to co robi client.
        '''
        out_player = []

        recived = {} 
        for key,value in self.connections.items():
            try:
                get_len = int(value[0].recv(5).decode("ascii"))
                recived[key] = json.loads(value[0].recv(get_len).decode("ascii"))
            except ConnectionResetError:
                # Jesli polaczenie zostalo zerwane(gracz wyszedl z gry) to usuwamy go z listy graczy na serwerze.
                out_player.append(key)

        for key in out_player:
            self.delete_connection(key)

        return recived
           
           
