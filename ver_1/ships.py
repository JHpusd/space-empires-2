class Ship():
    def update_coord(self, new_coords):
        self.coords = new_coords

class Scout(Ship):
    def __init__(self, player_num, init_coords):
        self.player_num = player_num
        self.max_hp = 1
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.cls = "E"
        self.coords = init_coords

class BattleCruiser(Ship):
    def __init__(self, player_num, init_coords):
        self.player_num = player_num
        self.max_hp = 2
        self.hp = 2
        self.atk = 5
        self.df = 1
        self.cls = "B"
        self.coords = init_coords