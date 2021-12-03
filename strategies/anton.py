from random import random
import math


class AntonStrat:
  def __init__(self):
    self.simple_board = {}
  
  def update_simple_board(self, updated_board):
    self.simple_board = updated_board

  def get_opponent_ships(self, ship_info, combat_order_info):
    return [obj_info for obj_info in combat_order_info if obj_info['player_num'] != ship_info['player_num'] and obj_info['hp'] > 0]

  def get_opponent_ships_on_space(self, ship_info, coords):
    if coords in self.simple_board.keys():
      return [obj_info for obj_info in self.simple_board[coords] if obj_info['player_num'] != ship_info['player_num'] and obj_info['obj_type'] == 'Ship' and obj_info['hp'] > 0]
    else:
      return []

  def calc_distance(self, point_1, point_2):
    return (abs(point_2[0]-point_1[0])**2 + abs(point_2[1]-point_1[1])**2)**0.5

  def find_home_colonies(self, ship_info):
    coords = []
    for coord in self.simple_board:
      for obj_info in self.simple_board[coord]:
        is_opponent_home_colony = obj_info['obj_type'] == 'Colony' and obj_info['is_home_colony'] and obj_info['player_num'] != ship_info['player_num']
        if is_opponent_home_colony:
          coords.append(coord)

    return coords

  def find_min_choice(self, choices, coord):
    min_choice = choices[0]
    min_distance = self.calc_distance(min_choice, coord)

    for choice in choices:
      if self.calc_distance(choice, coord) < min_distance:
        min_choice = choice
        min_distance = self.calc_distance(choice,coord)
    return min_choice

  def min_distance_translation(self, choices, ship_info, target_coords):
    if choices != []:
      min_choice = choices[0]
      min_distance = self.calc_distance((ship_info['coords'][0] + min_choice[0], ship_info['coords'][1] + min_choice[1]), target_coords)
      for choice in choices:
        current_coords = (ship_info['coords'][0] + choice[0], ship_info['coords'][1] + choice[1])
        current_distance = self.calc_distance(current_coords, target_coords)

        if current_distance < min_distance:
          min_distance = current_distance
          min_choice = choice
      
      return min_choice


  def check_for_opponents(self, ship_info, coords):
    for obj_info in self.simple_board[coords]:
      if obj_info['player_num'] != ship_info['player_num'] and obj_info['obj_type'] == 'Ship':
        return True
    return False
  
  def check_all_dreadnaughts(self, ship_info, opponent_ship_infos):
    for opponent_ship_info in opponent_ship_infos:
      if opponent_ship_info['name'] != "Dreadnaught":
        return False
    return True
  
  def check_for_adjacent_opponents(self, ship_info):
    adjacent_opponents = []
    coords = ship_info['coords']
    adjacent_translations = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    
    for translation in adjacent_translations:
      adjacent_coords = (coords[0] + translation[0], coords[1] + translation[1])
      if adjacent_coords in list(self.simple_board.keys()) and self.check_for_opponents(ship_info, adjacent_coords):
        adjacent_opponents.append(translation)
    return adjacent_opponents
  
  def get_priority_score(self, ship_info, opponent_ship_info):
    threat_level = opponent_ship_info['atk']*opponent_ship_info['hp'] + opponent_ship_info['df']
    vulnerability_level = 10/(opponent_ship_info['hp']) - 2*opponent_ship_info['df'] + ship_info['atk']**2
    chance = (ship_info['atk']-opponent_ship_info['df'])/10
    return (threat_level+vulnerability_level)*chance**4

  def choose_translation(self, ship_info, choices):
    ship_coords = ship_info['coords']
    player_num = ship_info['player_num']
    target_coords = self.find_min_choice(self.find_home_colonies(ship_info), ship_coords)
    best_translation = self.min_distance_translation(choices, ship_info, target_coords)

    adjacent_opponents = self.check_for_adjacent_opponents(ship_info)
    potential_coords = (ship_coords[0] + best_translation[0], ship_coords[1] + best_translation[1])
    opponent_ship_infos = self.get_opponent_ships_on_space(ship_info, potential_coords)
    all_dreadnaughts = self.check_all_dreadnaughts(ship_info, opponent_ship_infos)

    if len(adjacent_opponents) == 0 or not all_dreadnaughts or len(opponent_ship_infos)<8:
      return best_translation
    elif best_translation in adjacent_opponents:
      return (0,0)
    

  def choose_target(self, ship_info, combat_order_info):
    opponent_ship_infos = self.get_opponent_ships(ship_info,combat_order_info)
    highest_priority = []
    
    for _ in range(math.ceil(len(opponent_ship_infos)/3)):
      max_ship_info = opponent_ship_infos[0]
      max_score = 0

      for opponent_ship_info in opponent_ship_infos:
        ship_score = self.get_priority_score(ship_info, opponent_ship_info)
        if ship_score > max_score:
          max_ship_info = opponent_ship_info
          max_score = ship_score
      opponent_ship_infos.remove(max_ship_info)
      highest_priority.append(max_ship_info)
    
    random_idx = math.floor(len(highest_priority) * random())
    return highest_priority[random_idx]

  def buy_ships(self, cp_budget):
    return {'Dreadnaught':8}