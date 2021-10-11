class Ship():
    def update_coords(self, new_coords):
        self.coords = new_coords

class Scout(Ship):
    def __init__(self, player_num, init_coords, p_num, id_num):
        self.name = "Scout"
        self.player_num = player_num
        self.max_hp = 1
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.ship_class = "E"
        self.coords = init_coords
        self.p_num = p_num
        self.id_num = id_num
        self.obj_type = "Ship"

class BattleCruiser(Ship):
    def __init__(self, player_num, init_coords, p_num, id_num):
        self.name = "BattleCruiser"
        self.player_num = player_num
        self.max_hp = 2
        self.hp = 2
        self.atk = 5
        self.df = 1
        self.ship_class = "B"
        self.coords = init_coords
        self.p_num = p_num
        self.id_num = id_num
        self.obj_type = "Ship"