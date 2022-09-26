class Player:
    def __init__(self,nick):
        self.nick = nick
        self.position_x = 100
        self.position_y = 100
        self.level = 1
        self.life_points = 100
        self.v_x = 0
        self.v_y = 0
        self.direction_x = 1
        self.direction_y = 0
        self.FOV_x = 100

    def shoot(self):
        pass

    def convert_to_dict(self):
        return {
            "nick": self.nick,
            "position_x": self.position_x, 
            "position_y": self.position_y, 
            "level": self.level, 
            "life_points": self.life_points,  
            "v_x": self.v_x,  
            "v_y": self.v_y,  
            "direction_x": self.direction_x,  
            "direction_y": self.direction_y,
            "FOV_x": self.FOV_x  
        }
    
class Board:
    def __init__(self):
        self.width = 20
        self.height = 20

        def check_if_wall(i, j, size1, size2):
            if i == 0 or j == 0 or i == size1 - 1 or j == size2 - 1:
                return 1
            return 0
        self.square_board = [[check_if_wall(i, j, self.width, self.height) for i in range(self.width)] for j in range(self.height)]

        self.players = []

        self.bullets = []

        self.money = []

    def add_player(self,nick):
        self.players.append(Player(nick))

    def __str__(self): 
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += str(self.tab[i][j])
            out += '\n'
            
        return out

    def convert_to_dict(self, send_walls = False):
        if send_walls:
            return {"board" : self.square_board}
        
        return {
            "players": [player.convert_to_dict() for player in self.players],
            "bullets": [bullets.convert_to_dict() for bullets in self.bullets],
            "money": [money.convert_to_dict() for money in self.money]
        }

    def get_square_board (self):
        return self.square_board


class Bullet:
    def __init__(self,position_x,position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.v_x = 5
        self.v_y = 5
        self.color = (0,0,0)
        self.damage = 10

    def convert_to_dict(self):
        return {
            "position_x": self.position_x, 
            "position_y": self.position_y, 
            "v_x": self.v_x, 
            "v_y": self.v_y, 
            "color": self.color, 
            "damage": self.damage, 
        }
        



def main():
    import json


    game_board = Board()

    player1 = Player("Adam")
    bullet1 = Bullet(1,0)

    game_board.players.append(player1)
    game_board.bullets.append(bullet1)

    print(json.dumps(game_board.convert_to_dict()))

    

if __name__ == "_main_":
    main()