import math, random

class CaydenStrat():
    def __init__(self):
        self.simple_board = None

    def best_option(self, options, coordinate):
        best_option = options[0]
        min_distance = math.dist(best_option, coordinate)

        for option in options:
            if math.dist(option, coordinate) < min_distance:
                best_option = option
                min_distance = self.distance(option, coordinate)

        return best_option

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

    def choose_translation(self, ship_info, possible_translations):
        opponent_home_colony = []

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony.append(key)

        closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
        best_translation = self.best_translation(possible_translations, ship_info['coords'], closest_colony)

        if self.is_enemy_in_translation(ship_info, best_translation):
            return (0, 0)

        else:
            return best_translation

    def get_enemies(self, own_ship, combat_order):
        player_num = own_ship['player_num']
        enemies = []

        for ship_info in combat_order:
            if ship_info['player_num'] != player_num and ship_info['hp'] > 0:
                enemies.append(ship_info)

        return enemies


    def choose_target(self, ship_info, combat_order):
        enemies = self.get_enemies(ship_info, combat_order)
        return enemies[-1]