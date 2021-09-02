import math, sys, random
sys.path.append('ver_1')
from colony import *
from ships import *

def calc_distance(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return math.sqrt(dx**2 + dy**2)

class CustomPlayer():
    def __init__(self):
        self.player_num = None
        self.ships = []
        self.home_col = None
        self.colonies = []
    
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
    
    def distance(self, coord_1, coord_2):
        return math.sqrt(sum([(coord_1[i]-coord_2[i])**2 for i in range(len(coord_1))]))
    
    def min_distance_choice(self, choices, coord):
        best_choice = choices[0]
        min_distance = self.distance(best_choice, coord)

        for choice in choices:
            if self.distance(choice, coord) < min_distance:
                best_choice = choice
                min_distance = self.distance(choice,coord)
        return best_choice

    def min_distance_translation(self, choices, coord, target_coord):
        best_choice = choices[0]
        new_coord = self.list_add(best_choice, coord)
        dist = self.distance(new_coord, target_coord)
        for choice in choices:
            new_coord_2 = self.list_add(choice, coord)
            if self.distance(new_coord_2, target_coord) < dist:
                best_choice = choice
                new_coord = new_coord_2
                dist = self.distance(new_coord_2, target_coord)
        return best_choice
    
    def list_add(self, x, y):
        return [x[i]+y[i] for i in range(len(x))]

    def choose_translation(self, ship_coords, choices, opp_home_cols):
        print(choices)
        print(opp_home_cols)
        closest_col = self.min_distance_choice(opp_home_cols, ship_coords)
        return self.min_distance_translation(choices, ship_coords, closest_col)
    
    def choose_target(self, enemies):
        if len(enemies)==1:
            return enemies[0]
        return enemies[random.randint(0, len(enemies)-1)]
