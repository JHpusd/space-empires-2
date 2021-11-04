import random, math

class CharlieStrat:
    def __init__(self):
        self.simple_board = None

    def current_dist(self, coords_1, choice, coords_2):
        new_point = (coords_1[0] + choice[0], coords_1[1] + choice[1])
        return math.dist(new_point, coords_2)

    def min_distance_translation(self, ship_info, choices, target_coords):

        if choices != []:
            
            min_choice = choices[0]
            min_distance = self.current_dist(ship_info['coords'], min_choice, target_coords)

            for choice in choices:

                current_distance = self.current_dist(ship_info['coords'], choice, target_coords)

                if current_distance < min_distance:
                    min_distance = current_distance
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