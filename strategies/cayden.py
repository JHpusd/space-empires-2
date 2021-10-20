import math
import random

class CustomStrategy():
    def __init__(self):
        self.simple_board = None

    def calculate_distance(self, initial_point, ending_point):
        x = ending_point[0] - initial_point[0]
        y = ending_point[1] - initial_point[1]
        return (x ** 2 + y ** 2) ** 0.5

    def best_option(self, options, coordinate):
        best_option = options[0]
        min_distance = self.calculate_distance(best_option, coordinate)

        for option in options:
            if self.calculate_distance(option, coordinate) < min_distance:
                best_option = option
                min_distance = self.distance(option, coordinate)

        return best_option

    def best_translation(self, options, coordinate, desired_location):
        best_option = options[0]
        updated_coordinate = [best_option[n] + coordinate[n] for n in range(len(best_option))]
        distance = self.calculate_distance(updated_coordinate, desired_location)

        for option in options:
            new_coordinate = [option[n] + coordinate[n] for n in range(len(option))]

            if self.calculate_distance(new_coordinate, desired_location) < distance:
                best_option = option
                updated_coordinate = new_coordinate
                distance = self.calculate_distance(new_coordinate, desired_location)

        return best_option

    def choose_translation(self, ship_info, possible_translations):
        opponent_home_colony = []

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony.append(key)

        closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
        return self.best_translation(possible_translations, ship_info['coords'], closest_colony)

    def choose_target(self, ship_info, combat_order):
        enemies = []

        for ship in combat_order:
            if ship_info['player_num'] != ship['player_num']:
                enemies.append(ship)

        if len(enemies) == 1:
            return enemies[0]

        return enemies[random.randint(0, len(enemies) - 1)]