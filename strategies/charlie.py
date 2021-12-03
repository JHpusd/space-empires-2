import random, math, sys
sys.path.append('')
from ship_data import *

class CharlieStrat:
    def __init__(self):
        self.simple_board = None
    
    def current_dist(self, ship_coords, choice, target_coords):
        new_point = (ship_coords[0] + choice[0], ship_coords[1] + choice[1])
        return math.dist(new_point, target_coords)

    def min_distance_translation(self, ship_info, choices, target_coords):

        if choices != []:
            
            min_choice = None
            min_distance = 99999999

            for choice in choices:

                distance = self.current_dist(ship_info['coords'], choice, target_coords)

                if distance < min_distance:
                    min_distance = distance
                    min_choice = choice

            return min_choice

    def get_opponent_home_colony_coords(self, ship_info):
        for key, value in self.simple_board.items():
            for info in value:
                if info['obj_type'] == 'Colony' and info['is_home_colony'] and info['player_num'] != ship_info['player_num']:
                    return key

    def choose_translation(self, ship_info, choices):
        opponent_home_colony_coords = self.get_opponent_home_colony_coords(ship_info)
        return self.min_distance_translation(ship_info, choices, opponent_home_colony_coords)
        
    def choose_target(self, ship_info, simplified_combat_order):
        for info in simplified_combat_order:
            if info['player_num'] != ship_info['player_num']:
                return info
            
    def buy_ships(self, cp_budget):
        
        return {'Dreadnaught': 8, 'Scout': 1}
        # return {'Scout': 3, 'BattleCruiser': 3}
        
        # all_ship_names = str(all_ship_infos_dict)[1:-1]

        # player_wants_more_ships = True
        # player_ships = {}
        
        # while player_wants_more_ships:
            
        #     ship_name = input(f'Ship options: {all_ship_names}, none\nWhat ship do you want? ')
            
        #     if ship_name == 'none':
        #         player_wants_more_ships = False
        #         break

        #     if ship_name not in all_ship_names:
        #         print('That is not a ship!')
            
        #     else:
        #         player_ships[ship_name] = int(input('How many of that ship do you want? '))

        # print(f'\n your ships: {player_ships}\n')

        # return player_ships