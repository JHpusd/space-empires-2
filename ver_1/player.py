import math, sys, random
sys.path.append('ver_1')
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
    
    def set_home_col(self, col_coords):
        assert self.player_num != None, "player number needs to be set"
        self.home_col = Colony(self.player_num, col_coords)
    
    def add_colonies(self, col_list):
        assert self.player_num != None, "player number needs to be set"
        for col in col_list:
            self.colonies.append(col)

    def set_player_number(self, n):
        self.player_num = n

    def choose_translation(self, ship_coords, choices, opp_home_cols):
        return self.strategy.choose_translation(ship_coords,choices,opp_home_cols)
    
    def choose_target(self, enemies):
        return self.strategy.choose_target(enemies)
