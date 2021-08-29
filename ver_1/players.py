import math, sys
sys.path.append('ver_1')
from colony import *
from ships import *

def calc_distance(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return math.sqrt(dx**2 + dy**2)

class CustomPlayer():
    def __init__(self):
        self.player_number = None
        self.ships = []
        self.home_col = None
        self.colonies = []
    
    def add_ships(self, ship_list):
        assert self.player_number != None, "player number needs to be set"
        for ship in ship_list:
            self.ships.append(ship)
    
    def set_home_col(self, col_coords):
        assert self.player_number != None, "player number needs to be set"
        self.home_col = Colony(self.player_number, col_coords)
    
    def add_colonies(self, col_list):
        assert self.player_number != None, "player number needs to be set"
        for col in col_list:
            self.colonies.append(col)

    def set_player_number(self, n):
        self.player_number = n
    
    def distance(coord_1, coord_2):
        return math.sqrt(sum([coord_1[i]-coord_2[i] for i in range(len(coord_1))))
    
    def min_distance_choice(choices, coord):
        if target_coord == None:
            best_choice = choices[0]
            min_distance = distance(best_choice, coord)

            for choice in choices:
                if distance(choice, coord) < min_distnace:
                    best_choice = choice
                    min_distance = distance(choice,coord)
            return best_choice

    def min_distance_translation(choices, coord, target_coord):
        best_choice = choices[0]
        new_coord = list_add(best_choice, coord)
        dist = distance(new_coord, target_coord)
        for choice in choices:
            new_coord_2 = list_add(choice, coord)
            if distance(new_coord_2, target_coord) < dist:
                best_choice = choice
                new_coord = new_coord_2
                dist = distance(new_coord_2, target_coord)
        return best_choice
    
    def list_add(x, y):
        return [x[i]+y[i] for i in range(len(x))]

    def choose_translation(self, opp_home_cols, ship_coords, choices):
        closest_col = min_distance_choice(opp_home_cols, ship_coords)
        return min_distance_translation(choices, ship_coords, closest_col)
