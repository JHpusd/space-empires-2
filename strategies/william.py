import sys
sys.path.append('ver_3')
import math,random
from ship_data import *

class WilliamStrat:
  def __init__(self):
    self.simple_board = None
    self.num_runs = 0
  
  def choose_translation(self, ship_info, possible_translations):
    my_ship_coords = ship_info['coords']
    my_ship_num = ship_info['ship_num']
    op_player_num = 1 if ship_info['player_num'] == 2 else 2
    self.num_runs += 1

    for coord in self.simple_board:
      for obj in self.simple_board[coord]:
        if obj['obj_type'] == 'Colony':
          if obj['is_home_colony'] == True and obj['player_num'] == ship_info['player_num']:
            my_hc_coords = obj['coords']
          if obj['is_home_colony'] == True and obj['player_num'] == op_player_num:
            opp_hc_coords = obj['coords']
            
    if ship_info['name'] == 'Dreadnaught':
      if my_ship_num == 4:
        if my_hc_coords == (3,0):
          return (0,1)
        if my_hc_coords == (3,6):
          return (0,-1)
      if my_ship_coords == my_hc_coords:
        if my_hc_coords == (3,0):
          if my_ship_num == 1:
            return (0,1)
          if my_ship_num == 2:
            return (1,0)
          if my_ship_num == 3:
            return (-1,0)
        if my_hc_coords == (3,6):
          if my_ship_num == 1:
            return (0,-1)
          if my_ship_num == 2:
            return (1,0)
          if my_ship_num == 3:
            return (-1,0)
      else:
        return (0,0)

    if ship_info['name'] == 'Cruiser':
      if my_hc_coords == (3,0):
        if my_ship_num == 1:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (0,0):
              return (-1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,1)
        
        if my_ship_num == 2:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (1,0):
              return (-1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,1)
        
        if my_ship_num == 3:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (2,0):
              return (-1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,1)

        if my_ship_num == 4:
          return (0,1)
        
        if my_ship_num == 5:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (4,0):
              return (1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,1)
        
        if my_ship_num == 6:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (5,0):
              return (1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,1)
        
        if my_ship_num == 7:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (6,0):
              return (1,0)
            else:
              return (0,1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,1)

      elif my_hc_coords == (3,6):
        if my_ship_num == 1:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (0,6):
              return (-1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,-1)
        
        if my_ship_num == 2:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (1,6):
              return (-1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,-1)
        
        if my_ship_num == 3:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (2,6):
              return (-1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (1,0)
          else:
            return (0,-1)

        if my_ship_num == 4:
          return (0,-1)
        
        if my_ship_num == 5:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (4,6):
              return (1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,-1)
        
        if my_ship_num == 6:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (5,6):
              return (1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,-1)
        
        if my_ship_num == 7:
          if my_ship_coords[1] == my_hc_coords[1]:
            if my_ship_coords != (6,6):
              return (1,0)
            else:
              return (0,-1)
          elif my_ship_coords[1] == opp_hc_coords[1]:
            return (-1,0)
          else:
            return (0,-1)

    if my_hc_coords == (3,0):
      return (0,1)
    elif my_hc_coords == (3,6):
      return (0,-1)
      
      

  def choose_target(self, ship_info, combat_order): #ship-info = atacker
    possible_targets = self.filter_own_ships(ship_info['player_num'], combat_order)
    return possible_targets[random.randint(0,len(possible_targets)-1)]   
  
  def filter_own_ships(self, own_player_num, combat_order, ship_type=None):
    if ship_type is None:
        return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num]
    else:
        return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num and ship_dict['name'] == ship_type]

  def buy_ships(self, cp_budget):
    bought_ships = {'Scout': 1, 'Battlecruiser': 0, 'Battleship': 0, 'Cruiser': 10, 
      'Destroyer': 0, 'Dreadnaught': 3}
    return bought_ships
    
  def get_cp_of_dict(self, ships_dict):
    total_cp = 0
    for key in ships_dict:
      for ship in all_ship_infos:
        if ship['name'] == key:
          total_cp += ships_dict[key]*ship['cp_cost']
    return total_cp