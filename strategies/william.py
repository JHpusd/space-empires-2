import math,random

class WilliamStrat():
  def __init__(self):
    self.simple_board = None
    self.num_runs = 0
  
  def choose_translation(self, ship_info, possible_translations):
    self.num_runs += 1
    my_ship_coords = ship_info['coords']
    op_player_num = 1 if ship_info['player_num'] == 2 else 2

    for coord in self.simple_board:
      for obj in self.simple_board[coord]:
        if obj['obj_type'] == 'Colony':
          if obj['is_home_colony'] == True and obj['player_num'] == op_player_num:
            opp_hc_coords = obj['coords']

    if ship_info['player_num'] != 1:
      if self.num_runs < 7:
        return (0,0)

    best_translation = possible_translations[0]

    for translation in possible_translations:
      choice_coords = (my_ship_coords[0]+translation[0], my_ship_coords[1]+translation[1])
      best_coords = (my_ship_coords[0]+best_translation[0], my_ship_coords[1]+best_translation[1])
      choice_distance = math.dist(choice_coords, opp_hc_coords)
      best_distance = math.dist(best_coords, opp_hc_coords)

      if choice_distance < best_distance:
        best_translation = translation
    
    return best_translation
  
  def choose_target(self, ship_info, combat_order): #ship-info = atacker
    possible_targets = self.filter_own_ships(ship_info['player_num'], combat_order)
    return possible_targets[random.randint(0,len(possible_targets)-1)]   
  
  def filter_own_ships(self, own_player_num, combat_order, ship_type=None):
    if ship_type is None:
        return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num]
    else:
        return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num and ship_dict['name'] == ship_type]