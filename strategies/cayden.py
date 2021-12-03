import math, random
from ship_data import *

class CaydenStrat():
    def __init__(self):
        self.simple_board = None

    def best_translation(self, options, coordinate, desired_location):
        best_option = options[0]
        updated_coordinate = [best_option[n] + coordinate[n] for n in range(len(best_option))]
        distance = math.dist(updated_coordinate, desired_location)

        for option in options:
            new_coordinate = [option[n] + coordinate[n] for n in range(len(option))]

            if math.dist(new_coordinate, desired_location) < distance:
                best_option = option
                updated_coordinate = new_coordinate
                distance = math.dist(new_coordinate, desired_location)

        return best_option

    def is_enemy_in_translation(self, ship_info, translation):
        moving_to_coord = (ship_info['coords'][0] + translation[0], ship_info['coords'][1] + translation[1])

        if moving_to_coord in [key for key in self.simple_board]:
            for obj in self.simple_board[moving_to_coord]:
                if obj['player_num'] != ship_info['player_num'] and obj['obj_type'] == 'Ship':
                    return True

                else:
                    return False

        if moving_to_coord not in [key for key in self.simple_board]:
            return False

    def get_all_ships(self, player_number):
        ships = []

        for coordinate in self.simple_board:
            for obj in self.simple_board[coordinate]:
                if obj['obj_type'] == 'Ship' and obj['player_num'] == player_number:
                    ships.append(obj)

    def get_around_colony_coordinates(self, home_colony_coords, player_num):
        if home_colony_coords == (3, 0):
            return [(2, 0), (4, 0), (3, 1)]

        if home_colony_coords == (3, 6):
            return [(2, 6), (4, 6), (3, 5)]

    def enemy_ships_left(self, player_number):
        for coordinate in self.simple_board:
            for obj in self.simple_board[coordinate]:
                if obj['player_num'] != player_number and obj['obj_type'] == 'Ship':
                    return True

        return False

    def get_best_translation(self, ship_info, possible_translations):
        opponent_home_colony = []

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony.append(key)

        closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
        best_translation = self.best_translation(possible_translations, ship_info['coords'], closest_colony)

        return best_translation

    def are_my_ships_in_coord(self, coordinate, player_number):
        if coordinate not in list(self.simple_board.keys()):
            return False

        for obj in self.simple_board[coordinate]:
            if obj['player_num'] == player_number and obj['obj_type'] == 'Ship':
                return True

        return False

    def get_next_best_translation(self, ship_info, possible_translations, wanted_location):
        min_distance = 100
        min_distance_translation = possible_translations[0]

        for translation in possible_translations:
            if math.dist((translation[0] + ship_info['coords'][0], translation[1] + ship_info['coords'][1]), wanted_location) < min_distance:
                min_distance = math.dist((translation[0] + ship_info['coords'][0], translation[1] + ship_info['coords'][1]), wanted_location)
                min_distance_translation = translation

        return min_distance_translation

    def get_my_ships_in_coordinate(self, player_number, coordinate):
        my_ships = []

        if coordinate not in list(self.simple_board.keys()):
            return my_ships

        for obj in self.simple_board[coordinate]:
            if obj['obj_type'] == 'Ship' and obj['player_num'] == player_number:
                my_ships.append(obj)

        return my_ships
    
    def get_optimal_translation(self, ship_info, possible_translations, wanted_location):
        for translation in possible_translations:
            if (ship_info['coords'][0] + translation[0], ship_info['coords'][1] + translation[1]) == wanted_location:
                return translation

    def choose_translation(self, ship_info, possible_translations):
        opponent_home_colony = None
        my_home_colony_coords = None

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony = key

                if obj['obj_type'] == 'Colony' and obj['player_num'] == ship_info['player_num'] and obj['is_home_colony'] == True:
                    my_home_colony_coords = key

        best_translation = self.best_translation(possible_translations, ship_info['coords'], opponent_home_colony)

        if not self.enemy_ships_left(ship_info['player_num']):
            return best_translation


        if ship_info['name'] == 'Scout' and self.is_enemy_in_translation(ship_info, best_translation):
            other_translations = [translation for translation in possible_translations if translation != best_translation and translation != (0, 0)]
            return self.get_next_best_translation(ship_info, other_translations, opponent_home_colony)

        if ship_info['name'] == 'Scout' and not self.is_enemy_in_translation(ship_info, best_translation):
            if ship_info['player_num'] == 1:
                if self.are_my_ships_in_coord((ship_info['coords'][0], ship_info['coords'][1] + 2), 2) or self.are_my_ships_in_coord((ship_info['coords'][0], ship_info['coords'][1] + 1), 2): #their ships
                    return self.get_next_best_translation(ship_info, [translation for translation in possible_translations if translation != best_translation and translation != (0, 0)], opponent_home_colony)

            return best_translation

        if ship_info['name'] == 'Dreadnaught' and self.enemy_ships_left(ship_info['player_num']):
            defense_coordinates = self.get_around_colony_coordinates(my_home_colony_coords, ship_info['player_num'])
            return self.get_optimal_translation(ship_info, possible_translations, defense_coordinates[-1])

    def get_enemies(self, own_ship, combat_order):
        player_num = own_ship['player_num']
        enemies = []

        for ship_info in combat_order:
            if ship_info['player_num'] != player_num and ship_info['hp'] > 0:
                enemies.append(ship_info)

        return enemies

    def choose_target(self, ship_info, combat_order):
        enemies = self.get_enemies(ship_info, combat_order)
        return enemies[0]

    def buy_ships(self, cp_budget):
        return {'Dreadnaught': 8, 'Scout': 1}