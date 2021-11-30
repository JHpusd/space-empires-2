import math, random, sys
sys.path[0] = '/workspace/space-empires-2'
from ship_info import *

class CompetitionStrat:
    def __init__(self):
        self.simple_board = {}
        self.player_num = None
        self.turn = 0
        self.flank_moves = [(-1,0), (1,0)]
        self.ships = None

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
        new_coord = self.list_add(best_choice, coord)
        dist = self.distance(new_coord, target_coord)
        for choice in choices:
            new_coord_2 = self.list_add(choice, coord)
            if self.distance(new_coord_2, target_coord) < dist:
                best_choice = choice
                new_coord = new_coord_2
                dist = self.distance(new_coord_2, target_coord)
        return best_choice
    
    def list_add(self, x, y):
        return (x[0]+y[0], x[1]+y[1])
    
    def enemy_in(self, coord):
        if coord not in list(self.simple_board.keys()):
            return False
        for obj in self.simple_board[coord]:
            if obj['player_num']!=self.player_num and obj['obj_type']=='Ship':
                return True
        return False                

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
        move = self.min_distance_translation(choices, ship_coords, closest_col)
        '''
        if self.enemy_in(self.list_add(ship_coords, move)):
            return (0,0)
        '''
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
    def num_ships(self, ship_dict):
        return sum([ship_dict[key] for key in ship_dict])

    def update_simple_board(self, updated_board):
        self.simple_board = updated_board
    
    def buy_ships(self, cp_budget): # make an actual strategy
        self.ships = {'BattleCruiser':2, 'Dreadnaught':7}
        self.flankers = 'BattleCruiser'
        return {'BattleCruiser':2, 'Dreadnaught':7}