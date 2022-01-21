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
        self.maint_cost = 1

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
        self.maint_cost = 2

class Battleship(Ship):
    def __init__(self, player_num, init_coords, ship_num):
        self.name = 'Battleship'
        self.player_num = player_num
        self.hp = 3
        self.atk = 5
        self.df = 2
        self.ship_class = "A"
        self.coords = init_coords
        self.ship_num = ship_num
        self.obj_type = "Ship"
        self.cp_cost = 20
        self.maint_cost = 3

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
        self.maint_cost = 2

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
        self.maint_cost = 1

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
        self.maint_cost = 3