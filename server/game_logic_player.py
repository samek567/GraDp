import imp
from game_logic_bullet import Bullet

class Player:
    def __init__(self,nick):
        self.nick = nick
        self.position_x = 300
        self.position_y = 300
        self.level = 1
        self.life_points = 100
        self.v_x = 0
        self.v_y = 0
        self.FOV_x = 500
        self.hit_box_radius = 100 # jezeli pocisk przeleci w odleglosci mniejszej niz hit_box_radius to zakladamy ze trafil postac.
        self.reactivity = 500
        self.shoot_time_break = 0.5
        self.time_to_shoot = 0
        self.bullet_velocity = 5

    def change_velocity(self,arrows_pressed, dt, board, square_size):
        breaking_coef = 0.9
        
        if arrows_pressed[0]: # do góry
            self.v_y -= self.reactivity * dt
        if arrows_pressed[1]: # W dol
            self.v_y += self.reactivity * dt
        if arrows_pressed[2]: # W lewo
            self.v_x -= self.reactivity * dt
        if arrows_pressed[3]: # W prawo
            self.v_x += self.reactivity * dt
        
        self.v_x *= breaking_coef
        self.v_y *= breaking_coef

        if abs(self.v_x) < self.reactivity * dt * breaking_coef * 0.5: 
            self.v_x = 0
        if abs(self.v_y) < self.reactivity * dt * breaking_coef * 0.5: 
            self.v_y = 0


        if board[int(self.position_y // square_size)][int((self.position_x + self.v_x * dt + ((self.v_x > 0) * 2 -1) * self.hit_box_radius) // square_size)] :
            self.v_x = 0
        if board[int((self.position_y + self.v_y * dt + ((self.v_y > 0) * 2 -1) * self.hit_box_radius) // square_size)][int(self.position_x // square_size)] :
            self.v_y = 0

        if board[int((self.position_y + self.hit_box_radius * 0.70710678118) // square_size)][int((self.position_x + self.hit_box_radius * ((self.v_x > 0) * 2 -1) * 0.70710678118 + dt * self.v_x) // square_size)]:
            self.v_x = 0

        if board[int((self.position_y - self.hit_box_radius * 0.70710678118) // square_size)][int((self.position_x + self.hit_box_radius * ((self.v_x > 0) * 2 -1) * 0.70710678118 + dt * self.v_x) // square_size)]:
            self.v_x = 0




        if board[int((self.position_y + self.hit_box_radius * ((self.v_y > 0) * 2 -1) * 0.70710678118 + dt * self.v_y) // square_size)][int((self.position_x - self.hit_box_radius * 0.70710678118) // square_size)]:
            self.v_y = 0

        if board[int((self.position_y + self.hit_box_radius * ((self.v_y > 0) * 2 -1) * 0.70710678118 + dt * self.v_y) // square_size)][int((self.position_x + self.hit_box_radius * 0.70710678118) // square_size)]:
            self.v_y = 0

    def move(self,dt):
        self.position_x += self.v_x * dt
        self.position_y += self.v_y * dt


    def try_to_shoot(self,direction):
        if self.time_to_shoot <= 0:
            self.time_to_shoot = self.shoot_time_break
            return Bullet(self.position_x,self.position_y,direction[0]*self.bullet_velocity,direction[1]*self.bullet_velocity)
        return 0

    def convert_to_dict(self):
        return {
            "nick": self.nick,
            "position_x": self.position_x, 
            "position_y": self.position_y, 
            "level": self.level, 
            "life_points": self.life_points,  
            "v_x": self.v_x,  
            "v_y": self.v_y,  
            "FOV_x": self.FOV_x,
            "hit_box_radius": self.hit_box_radius
        }