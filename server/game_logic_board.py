from math import inf
from game_logic_player import Player
from game_logic_bullet import Bullet

class Board:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.square_size = 100

        with open(".\\map.txt","r") as file:
            self.square_board = [line.split() for line in file.readlines()]

        for i in range(len(self.square_board)):
            for j in range(len(self.square_board[i])):
                self.square_board[i][j] = int(self.square_board[i][j])

        self.players = []

        self.bullets = []

        self.money = []

    def add_player(self,nick):
        self.players.append(Player(nick))
        
    def delete_player(self,nick):
        for i in range(len(self.players)):
            if self.players[i].nick == nick:
                self.players.pop(i)
                return 0

    def __str__(self): 
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += str(self.tab[i][j])
            out += '\n'
            
        return out

    def update(self, info_from_players, dt):
        '''
        To jest funkcja odpowiedzialna za fizykę całej gry.
        '''

        for player in self.players:
            if player.time_to_shoot > 0:
                player.time_to_shoot -= dt
            player.change_velocity(info_from_players[player.nick]["arrows_pressed"],dt,self.square_board,self.square_size)
            player.move(dt)
            if info_from_players[player.nick]["mouse_pressed"][0]:
                bullet = player.try_to_shoot(info_from_players[player.nick]["direction"])
                print(info_from_players[player.nick])
                if not (type(bullet) is int):
                    print("Dodajemy kule")
                    self.bullets.append(bullet)


    def convert_to_dict(self, send_walls = False):
        if send_walls:
            return {
                "board" : self.square_board,
                "square_size" : self.square_size
            }
        
        return {
            "players": {player.nick: player.convert_to_dict() for player in self.players},
            "bullets": [bullets.convert_to_dict() for bullets in self.bullets],
            "money": [money.convert_to_dict() for money in self.money]
        }

    def get_square_board (self):
        return self.square_board