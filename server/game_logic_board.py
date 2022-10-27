from math import inf
from turtle import width
from game_logic_player import Player
from game_logic_bullet import Bullet
import random

class Board:
    def __init__(self):
        self.square_size = 100

        with open(".\\map.txt","r") as file:
            self.square_board = [line.split() for line in file.readlines()]

        self.width = len(self.square_board[0])
        self.height = len(self.square_board)

        for i in range(len(self.square_board)):
            for j in range(len(self.square_board[i])):
                self.square_board[i][j] = int(self.square_board[i][j])

        self.players = [] # Tu trzymamy obiekty klasy players

        self.bullets = [] # Tu trzymamy obiekty klasy bullets

        self.money = [] # Tu trzymamy wspolrzedne pieniadza x i y

        for i in range(10):
            self.add_money()

    def add_player(self,nick):
        self.players.append(Player(nick))
        
    def delete_player(self,nick):
        for i in range(len(self.players)):
            if self.players[i].nick == nick:
                self.players.pop(i)
                return 0

    def add_money(self):
        while True:
            x = random.randint(self.square_size, self.square_size * (self.width - 1))
            y = random.randint(self.square_size,self.square_size * (self.height - 1))
            if self.square_board[y // self.square_size][x // self.square_size] == 0:
                break
        self.money.append((x,y))

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
            money_to_delete = []

            for coin in self.money:
                if (player.position_x - coin[0]) ** 2  + (player.position_y - coin[1]) ** 2 <= player.coin_grab_range ** 2:
                    player.budget+=1
                    money_to_delete.append(coin)
            
            for to_delete in money_to_delete:
                self.money.remove(to_delete)
                self.add_money()

            for bullet in self.bullets:
                if (player.position_x - bullet.position_x) ** 2  + (player.position_y - bullet.position_y) ** 2 <= player.hit_box_radius ** 2:
                    player.life_points -= 1

            if player.time_to_shoot > 0:
                player.time_to_shoot -= dt
            player.change_velocity(info_from_players[player.nick]["arrows_pressed"],dt,self.square_board,self.square_size)
            player.move(dt)
            if info_from_players[player.nick]["mouse_pressed"][0]:
                bullet = player.try_to_shoot(info_from_players[player.nick]["direction"])
                print(info_from_players[player.nick])
                if not (type(bullet) is int):
                    self.bullets.append(bullet)

        bullets_to_delete = []
        for i in range(len(self.bullets)):
            self.bullets[i].move(dt)
            if self.square_board[int(self.bullets[i].position_y // self.square_size)][int(self.bullets[i].position_x // self.square_size)]:
                bullets_to_delete.append(i)

        for i in range(len(bullets_to_delete)-1,-1,-1):
            self.bullets.pop(bullets_to_delete[i])
                



    def convert_to_dict(self, send_walls = False):
        if send_walls:
            return {
                "board" : self.square_board,
                "square_size" : self.square_size
            }
        
        return {
            "players": {player.nick: player.convert_to_dict() for player in self.players},
            "bullets": [bullets.convert_to_dict() for bullets in self.bullets],
            "money": self.money
        }

    def get_square_board (self):
        return self.square_board