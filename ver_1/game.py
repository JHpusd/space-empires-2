import math, random, sys, inspect
sys.path.append('logs')
from logger import *
sys.path.append('ver_1')
from colony import *
from ships import *

class Game:
    def __init__(self, players, board_size=[7,7], log_name='logs.txt'):
        self.logs = Logger('/home/runner/space-empires-2/logs/'+log_name)
        self.logs.clear_log()
        self.players = players
        self.set_player_numbers()

        self.board_size = board_size
        global board_x, board_y, mid_x, mid_y
        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2
        self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]

        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.set_up_game()
    
    def set_player_numbers(self):
        for i,player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.board_size
        x, y = coords
        dx, dy = translation
        new_coords = (x+dx,y+dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []
        for translation in translations:
            if self.check_if_translation_is_in_bounds(coords, translation):
                in_bounds_translations.append(translation)
        return in_bounds_translations
    
    def add(self, objs):
        if type(objs) is not list:
            objs = [objs]
        for obj in objs:
            coord = obj.coords
            self.board[coord[1]][coord[0]].append(obj)
        
    def delete(self, objs):
        if type(objs) is not list:
            objs = [objs]
        for obj in objs:
            coord = obj.coords
            self.board[coord[1]][coord[0]].remove(obj)
    
    def all_objects(self, coord):
        return self.board[coord[1]][coord[0]]
    
    def all_ships(self, coord):
        return [obj for obj in self.all_objects(coord) if isinstance(obj, Ship)]
    
    def set_up_game(self):
        starts = [(0, mid_x-1), (board_y-1, mid_x-1), (mid_y-1, 0), (mid_y-1, board_x-1)]
        for i in range(len(self.players)):
            player = self.players[i]
            player_num = self.players[i].player_num
            coord = starts[i]

            player.set_home_col(coord)
            self.add(player.home_col)
            for _ in range(3): # need to change if number of initial ships changes
                scout = Scout(player_num, coord)
                bc = BattleCruiser(player_num, coord)
                self.add([scout, bc])
                player.add_ships([scout, bc])
    
    def distance(self, obj_1, obj_2):
        coord_1 = obj_1.coords
        coord_2 = obj_2.coords
        return math.sqrt(sum([(coord_1[i]-coord_2[i])**2 for i in range(len(coord_1))]))

    def list_add(self, x,y):
        return [x[i]+y[i] for i in range(len(x))]
    
    def enemy_in_coord(self, ship):
        coord = ship.coords
        for obj in self.all_objects(coord):
            if obj.player_num != ship.player_num:
                if coord not in self.combat_coords:
                    self.combat_coords.append(coord)
                return True
        return False
    
    def move(self, ship, translation):
        new_coords = self.list_add(ship.coords, translation)
        self.delete(ship)
        ship.update_coords(new_coords)
        self.add(ship)
    
    def complete_move_phase(self):
        for player in self.players:
            opp_home_cols = [p.home_col.coords for p in self.players if p.player_num != player.player_num]
            for ship in player.ships:
                if self.enemy_in_coord(ship):
                    continue
                coords = ship.coords   
                choices = self.get_in_bounds_translations(coords)
                move = player.choose_translation(coords, choices, opp_home_cols)
                assert move in choices, "invalid move"
                self.move(ship, move)
                if self.enemy_in_coord(ship):
                    continue
    
    def roll(self):
        return random.randint(1,10)
    
    def hit(self, attacker, defender):
        assert attacker.hp > 0 and defender.hp > 0, "dead ship in combat"
        assert attacker.player_num != defender.player_num, "friendly fire not enabled"
        roll = self.roll()
        new_atk = attacker.atk - defender.df
        if roll <= new_atk:
            return True
        return False
    
    def remove_ship(self, ship):
        player = self.players[ship.player_num - 1]
        player.ships.remove(ship)
        self.delete(ship)
        
    def get_enemies(self, ship, combat_list):
        return [obj for obj in combat_list if obj.player_num != ship.player_num]
    
    def all_same_team(self, ship_list):
        return len(set([ship.player_num for ship in ship_list])) == 1

    def complete_combat_phase(self): # prioritization: class, tactics, first in square
        to_delete_coords = []
        for coord in self.combat_coords:
            by_cls = sorted(self.all_ships(coord), key=lambda x: x.cls)
            # by tactics (not yet available)
            # by chronological order is already built-in via appending
            for ship in by_cls:
                if ship.hp == 0:
                    continue
                player = self.players[ship.player_num - 1]
                enemies = self.get_enemies(ship, by_cls)
                target = player.choose_target(enemies)
                assert target in enemies, "target not in target list"
                if self.hit(ship, target):
                    target.hp -= 1
                    if target.hp == 0:
                        self.remove_ship(target)
            for ship in by_cls:
                if ship.hp == 0:
                    by_cls.remove(ship)
            if self.all_same_team(by_cls):
                to_delete_coords.append(coord)
        for coord in to_delete_coords:
            self.combat_coords.remove(coord)
                    


