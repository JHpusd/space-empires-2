import math, sys, random
from colony import *
from ships import *

def calc_distance(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return math.sqrt(dx**2 + dy**2)

class Player():
    def __init__(self, strategy_cls):
        self.player_num = None
        self.ships = []
        self.home_col = None
        self.colonies = []
        self.strategy = strategy_cls
    
    def add_ships(self, ship_list):
        assert self.player_num != None, "player number needs to be set"
        for ship in ship_list:
            self.ships.append(ship)
    
    def set_home_col(self, col_coords, id_num):
        assert self.player_num != None, "player number needs to be set"
        self.home_col = Colony(self.player_num, col_coords, id_num)
        self.home_col.obj_type = 'HomeColony'
    
    def add_colonies(self, col_list):
        assert self.player_num != None, "player number needs to be set"
        for col in col_list:
            self.colonies.append(col)

    def set_player_number(self, n):
        self.player_num = n

    def choose_translation(self, ship_info, choices):
        return self.strategy.choose_translation(ship_info,choices)
    
    def choose_target(self, ship_info, enemies_info):
        return self.strategy.choose_target(ship_info, enemies_info)
