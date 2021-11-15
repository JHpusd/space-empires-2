class Ship():
    def update_coords(self, new_coords):
        self.coords = new_coords

class Scout(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name = "Scout"
        self.player_num = player_num
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.ship_class = "E"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 6

class BattleCruiser(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name = "BattleCruiser"
        self.player_num = player_num
        self.hp = 2
        self.atk = 5
        self.df = 1
        self.ship_class = "B"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 15

class Cruiser(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name= "Cruiser"
        self.player_num = player_num
        self.hp = 2
        self.atk = 4
        self.df = 1
        self.ship_class = "C"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 12

class Destroyer(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name = "Destroyer"
        self.player_num = player_num
        self.hp = 1
        self.atk = 4
        self.df = 0
        self.ship_class = "D"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 9

class Dreadnaught(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name = "Dreadnaught"
        self.player_num = player_num
        self.hp = 3
        self.atk = 6
        self.df = 3
        self.ship_class = "A"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 24