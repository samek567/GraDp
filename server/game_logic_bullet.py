class Bullet:
    def __init__(self,position_x,position_y,v_x,v_y):
        self.position_x = position_x
        self.position_y = position_y
        self.v_x = v_x
        self.v_y = v_y
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
        