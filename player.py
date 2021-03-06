import math, sys, random
from colony import *
from ships import *
from ship_data import *

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
        self.cp = 0
        self.ship_counter = {key:0 for key in list(ship_objects.keys())}
    
    def add_ships(self, ship_list):
        assert self.player_num != None, "player number needs to be set"
        if type(ship_list) != list:
            ship_list = [ship_list]
        for ship in ship_list:
            self.ships.append(ship)
    
    def set_home_col(self, col_coords):
        assert self.player_num != None, "player number needs to be set"
        self.home_col = Colony(self.player_num, col_coords)
        self.home_col.is_home_colony = True
    
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
    
    def clear_all(self):
        self.player_num = None
        self.ships = []
        self.home_col = None
        self.colonies = []
        self.cp = 0
        self.ship_counter = {key:0 for key in list(ship_objects.keys())}
    
    def buy_ships(self, cp_budget):
        return self.strategy.buy_ships(cp_budget)