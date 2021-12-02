import math, random, sys
sys.path[0] = '/workspace/space-empires-2'
from ship_info import *

class CompetitionStrat:
    def __init__(self):
        self.simple_board = {}
        self.player_num = None
        self.col_coord = None

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
        new_coord = self.coord_add(best_choice, coord)
        dist = self.distance(new_coord, target_coord)
        for choice in choices:
            new_coord_2 = self.coord_add(choice, coord)
            if self.distance(new_coord_2, target_coord) < dist:
                best_choice = choice
                new_coord = new_coord_2
                dist = self.distance(new_coord_2, target_coord)
        return best_choice
    
    def coord_add(self, x, y):
        return (x[0]+y[0], x[1]+y[1])
    
    def enemy_in(self, coord):
        if coord not in list(self.simple_board.keys()):
            return False
        for obj in self.simple_board[coord]:
            if obj['player_num']!=self.player_num and obj['obj_type']=='Ship':
                return True
        return False   
    
    def ally_in(self, coord):
        if coord not in list(self.simple_board.keys()):
            return False
        for obj in self.simple_board[coord]:
            if obj['player_num']==self.player_num and obj['obj_type']=='Ship':
                return True
        return False 

    def enemy_adjacent(self, coord, deleted_options=[]):
        options = [(1,0),(-1,0),(0,1),(0,-1)]
        options = [option for option in options if option not in deleted_options]
        for option in options:
            new_coord = self.coord_add(option, coord)
            if self.enemy_in(new_coord):
                return True
        return False

    def get_flanker_coord(self, ship_coord, deleted_options=[]):
        options = [(1,0),(-1,0),(0,1),(0,-1)]
        options = [option for option in options if option not in deleted_options]
        for option in options:
            new_coord = self.coord_add(option, ship_coord)
            if self.enemy_in(new_coord) and self.num_total_ships(new_coord, 3-self.player_num) <= 3:
                return new_coord
        return None

    def num_ships(self, coord, player_num, ship_type): # counts number of a certain type of ship belonging to corresponding player in a coord
        if coord not in list(self.simple_board.keys()):
            return 0
        total = 0
        for ship_info in self.simple_board[coord]:
            if ship_info['obj_type']=='Colony':
                continue
            if ship_info['player_num']==player_num and ship_info['name']==ship_type:
                total += 1
        return total
    
    def num_total_ships(self, coord, player_num):
        if coord not in list(self.simple_board.keys()):
            return 0
        return len([item for item in self.simple_board[coord] if item['obj_type']=='Ship' and item['player_num']])

    def choose_translation(self, ship_info, choices): # move to opp colony, if enemy in move coord, dont move
        if self.player_num == None:
            self.player_num = ship_info['player_num']

        ship_coords = ship_info['coords']
        p_num = ship_info['player_num']
        opp_home_cols = []
        for key in self.simple_board:
            for item in self.simple_board[key]:
                if item['obj_type']=='Colony' and item['is_home_colony'] and item['player_num']!=p_num:
                    opp_home_cols.append(key)
        closest_col = self.min_distance_choice(opp_home_cols, ship_coords)

        if ship_info['name'] == self.flanker:
            return self.flanker_translation(ship_info, choices, closest_col)
        return self.attacker_translation(ship_info, choices, closest_col)
    
    def flanker_translation(self, ship_info, choices, target_coord):
        # make best moves but take evasive maneuvers if there is an enemy adjacent to the new coord
        ship_coords = ship_info['coords']
        choices.remove((0,0))
        while True:
            if len(choices) == 1:
                return choices[0]
            best_choice = self.min_distance_translation(choices, ship_coords, target_coord)
            new_coord = self.coord_add(ship_coords, best_choice)
            if self.enemy_adjacent(new_coord) or self.enemy_in(new_coord):
                choices.remove(best_choice)
                continue
            return best_choice
    
    def attacker_translation(self, ship_info, choices, target_coord):
        coords = ship_info['coords']

        move = self.min_distance_translation(choices, coords, target_coord)
        new_coord = self.coord_add(coords, move)
        more_enemy_dreadnaughts = self.num_ships(new_coord,3-self.player_num,'Dreadnaught') >= 8

        if more_enemy_dreadnaughts and self.enemy_adjacent(coords, deleted_options=[move]):
            if self.get_flanker_coord(coords) != None:
                flanker_coords = self.get_flanker_coord(coords)
                if not self.ally_in(flanker_coords):
                    move = (flanker_coords[0]-coords[0], flanker_coords[1]-coords[1])

        if self.enemy_in(self.coord_add(coords, move)) and more_enemy_dreadnaughts:
            return (0,0)
        return move
    
    def get_enemies(self, own_ship, combat_order):
        player_num = own_ship['player_num']
        if self.player_num == None:
            self.player_num = player_num
        enemies = []
        for ship_info in combat_order:
            if ship_info['player_num'] != player_num and ship_info['hp'] > 0:
                enemies.append(ship_info)
        return enemies
    
    def hit_chance(self, attacker_info, defender_info):
        return (attacker_info['atk'] - defender_info['df']) / 10
    
    def threat(self, ship_info):
        return (ship_info['hp'] * ship_info['atk']) + ship_info['df']
    
    def vulnerability(self, ship_info):
        if ship_info['hp'] <= 0:
            print("vulnerability problem with dead ship")
            return None
        return (10/ship_info['hp']) - 2*ship_info['df']
    
    def maximize(self, choices, val_formula):
        best_item = choices[0]
        best_val = val_formula(best_item)
        for item in choices:
            if val_formula(item) > best_val:
                best_item = item
                best_val = val_formula(best_item)
        return item
    
    def target_weight(self, ship_info, target_info):
        chance = self.hit_chance(ship_info, target_info)
        threat = self.threat(target_info)
        vuln = self.vulnerability(target_info)
        return chance * threat * vuln

    '''
    def choose_target(self, ship_info, combat_order): # target weights
        enemies_info = self.get_enemies(ship_info, combat_order)

        best_target = enemies_info[0]
        highest_weight = self.target_weight(ship_info, best_target)
        for target in enemies_info:
            if self.target_weight(ship_info, target) > highest_weight:
                if abs(self.target_weight(ship_info, target)-highest_weight) <= 0.15*highest_weight:
                    best_target = random.choice([best_target, target])
                    highest_weight = self.target_weight(ship_info, best_target)
                    continue
                best_target = target
                highest_weight = self.target_weight(ship_info, best_target)
        return best_target
    '''
    def choose_target(self,ship_info,combat_order): # prioritization based on ship stat
        self.first_turn = False
        enemies_info = self.get_enemies(ship_info, combat_order)

        if ship_info['atk'] < 5: # prioritize vulnerability and hit chance
            f = lambda target: self.vulnerability(target)*self.hit_chance(ship_info,target)
            return self.maximize(enemies_info, f)
        else:
            f = lambda target: self.vulnerability(target)*self.threat(target)
            return self.maximize(enemies_info, f)
    '''
    def choose_target(self, ship_info, combat_order): # target first enemy
        enemies_info = self.get_enemies(ship_info, combat_order)
        return enemies_info[0]
    '''
    def update_simple_board(self, updated_board):
        self.simple_board = updated_board
        if self.simple_board == {} or self.player_num == None:
            return
        for key in self.simple_board:
            for item in self.simple_board[key]:
                if item['obj_type']=='Colony' and item['is_home_colony']==True and item['player_num']==self.player_num:
                    self.col_coord = item['coords']
    
    def buy_ships(self, cp_budget): # make an actual strategy
        self.flanker = 'Scout'
        return {'Scout':1, 'Dreadnaught':8}