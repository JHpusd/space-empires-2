## Compatable w/ strat_plr_2

import random as rand
import math

class MaiaStrat () :
    def __init__(self) :
        self.simple_board = {}
        self.all_to_me = False


    def buy_ships(self, cp_amount) :
        #ship_amounts = {'Destroyer': 6, 'Dreadnaught': 6}
        ship_amounts = {'Scout': 5, 'BattleCruiser': 0, 'Cruiser': 0, 'Destroyer': 0, 'Dreadnaught': 7}
        return ship_amounts

    def choose_translation(self, ship_info, choices) :
        if self.chosen_one(ship_info) :
            return self.chosen_one_mvmt(ship_info, choices)
        return self.gen_pop_mvmt(ship_info, choices)

    def choose_target(self, ship, current_battle) :
        plr_num = ship['player_num']

        opp_ships = [[],[]]
        ship_init = current_battle.index(ship)
        place = 0

        for index in range(len(current_battle)) :
            if index == ship_init :
                place = 1
            ship_info = current_battle[index]
            if ship_info['player_num'] != plr_num :
                opp_ships[place].append(ship_info)

        priority = []

        before = opp_ships[0]
        before.sort(key=(lambda a: a['hp']))
        priority.extend(before)

        after = opp_ships[1]
        after.sort(key=(lambda a: a['hp']))
        priority.extend(after)

        priority.sort(key=(lambda a: a['hp']))

        return priority[0]

    def chosen_one(self, candidate) :
        if candidate['coords'] != self.find_home_col(candidate['player_num']) :
            return True
        lowest_health = 100
        chosen_ship = None
        for ship in self.the_gang(candidate['player_num']) :
            if ship['hp'] < lowest_health :
                lowest_health = ship['hp']
                chosen_ship = ship
            if ship['coords'] != self.find_home_col(candidate['player_num']) :
                return False
        if candidate == chosen_ship :
            return True
        return False
    
    def translate(self, ship_dict_list) :
        readable = []
        for ship in ship_dict_list :
            ship_stuff = (ship['player_num'], ship['ship_id'], ship['hp'])
            readable.append(ship_stuff)
        print(readable)
        
    def find_home_col(self, plr_num) :
        for coord, stuff in self.simple_board.items() :
            for obj in stuff :
                if obj['player_num'] == plr_num and obj['obj_type'] == 'Colony' and obj['is_home_colony'] :
                    return coord
    
    def opp_there(self, plr_num, coord) :
        if coord not in self.simple_board.keys() :
            return False
        test = {ship_info['player_num'] for ship_info in self.simple_board[coord] if ship_info['obj_type'] == 'Ship'}
        if ((plr_num % 2) + 1) in test :
            return True
        return False
    
    def to_coords(self, ship_coords, colony_coords, choices = [(1,0),(0,1), (-1,0), (0,-1)]) :
        dist_sqr = (ship_coords[0] - colony_coords[0]) ** 2 + (ship_coords[1] - colony_coords[1]) ** 2
        best_mvmt = (0,0)

        for choice in choices :
            option = (choice[0] + ship_coords[0], choice[1] + ship_coords[1])
            option_dist_sqr = (option[0] - colony_coords[0]) ** 2 + (option[1] - colony_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_mvmt = choice
                dist_sqr = option_dist_sqr
        return best_mvmt

    def the_gang(self, plr_num) :
        gang = []
        for ship_list in self.simple_board.values() :
            for ship in ship_list :
                if ship['player_num'] == plr_num and ship['obj_type'] == 'Ship' :
                    gang.append(ship)
        return gang

    def chosen_one_mvmt(self, ship_info, choices) :
        coords = ship_info['coords']
        alt_id = (ship_info['player_num'] % 2) + 1
        alt_col = self.find_home_col(alt_id)

        if self.all_to_me :
            if coords != (alt_col[0]+1,alt_col[1]) and coords != (alt_col[0]-1,alt_col[1]) and coords != (alt_col[0],alt_col[1]+1) and coords != (alt_col[0],alt_col[1]-1) :
                return self.gen_pop_mvmt(ship_info, choices)
            for ship in self.the_gang(ship_info['player_num']) :
                if ship['coords'] != (alt_col[0]+1,alt_col[1]) and ship['coords'] != (alt_col[0]-1,alt_col[1]) and ship['coords'] != (alt_col[0],alt_col[1]+1) and ship['coords'] != (alt_col[0],alt_col[1]-1) and ship['coords'] != self.find_home_col(ship['player_num']) and ship['coords'] != alt_col:
                    return (0,0)
            return self.to_coords(coords, alt_col, choices)

        if coords == self.find_home_col(ship_info['player_num']) :
            return (1,0)
        
        mvmt = self.to_coords(coords, alt_col, choices)
        
        new_coords = (coords[0]+mvmt[0], coords[1]+mvmt[1])

        finish_him = False

        if new_coords == alt_col :
            finish_him = True
        
        while self.opp_there(ship_info['player_num'], new_coords) :
            if finish_him :
                self.all_to_me = True
                return (0,0)
            choices.remove(mvmt)
            mvmt = self.to_coords(coords, alt_col, choices) 
            if mvmt == (0,0) :
                if (0,0) in choices :
                    choices.remove((0,0))
                if choices == [] :
                    return (0,0)
                mvmt = choices[0]

            new_coords = (coords[0]+mvmt[0], coords[1]+mvmt[1])
        return mvmt

    def gen_pop_mvmt(self, ship_info, choices) :
        if not self.all_to_me :
            return (0,0)
        plr_num = ship_info['player_num']
        home_col = self.find_home_col(plr_num)
        coords = ship_info['coords']
        alt_id = (plr_num % 2) + 1
        alt_col = self.find_home_col(alt_id)

        if ship_info in self.simple_board[home_col] and len(self.simple_board[home_col]) == 2 :
            for choice in choices :
                if self.opp_there(plr_num, (home_col[0]+choice[0], home_col[1]+choice[1])) :
                    return (0,0)

        mvmt = self.to_coords(coords, alt_col, choices)

        new_coords = (coords[0]+mvmt[0], coords[1]+mvmt[1])

        #print(self.opp_there(plr_num, best_coord))

        while self.opp_there(plr_num, new_coords) :
            if new_coords == alt_col :
                return mvmt
            choices.remove(mvmt)
            mvmt = self.to_coords(coords, alt_col, choices) 
            if mvmt == (0,0) :
                if (0,0) in choices :
                    choices.remove((0,0))
                mvmt = choices[0]

            new_coords = (coords[0]+mvmt[0], coords[1]+mvmt[1])
        return mvmt