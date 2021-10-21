import math, random, sys
from colony import *
from ships import *
sys.path.append('logs')
from logger import *

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
        self.board = {}

        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.set_up_game()
        self.update_simple_boards()
    
    def set_player_numbers(self):
        for i,player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        if 0 <= x and x <= board_x-1:
            if 0 <= y and y <= board_y-1:
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
            if coord not in list(self.board.keys()):
                self.board[coord] = [obj]
                continue
            self.board[coord].append(obj)
        
    def delete(self, objs):
        if type(objs) is not list:
            objs = [objs]
        for obj in objs:
            coord = obj.coords
            if coord not in list(self.board.keys()):
                print("removing from invalid coord")
                return
            self.board[coord].remove(obj)
            if len(self.board[coord]) == 0:
                del self.board[coord]
    
    def all_ships(self, coord):
        return [obj for obj in self.board[coord] if isinstance(obj, Ship)]

    def set_up_game(self):
        if len(self.players) > 4:
            print("cannot have more than 4 players")
            self.logs.write('SETUP STOPPED')
            return
        starts = [(0, mid_x-1), (board_y-1, mid_x-1), (mid_y-1, 0), (mid_y-1, board_x-1)]
        self.logs.write(str(len(self.players))+' PLAYERS PLAYING\n')
        self.logs.write('SETTING UP GAME...\n')
        for i in range(len(self.players)):
            player = self.players[i]
            player_num = self.players[i].player_num
            coord = starts[i]
            self.logs.write('PLAYER '+str(player_num)+' STARTING AT '+str(coord)+'\n')
            player.set_home_col(coord)
            self.add(player.home_col)
            for i in range(3): # need to change if number of initial ships changes
                scout = Scout(player_num, coord, i+1)
                bc = BattleCruiser(player_num, coord, i+1)
                self.add([scout, bc])
                player.add_ships([scout, bc])
        self.logs.write('\n')
    
    def get_info(self, obj):
        return obj.__dict__
    
    def update_simple_boards(self):
        simple_board = {key:[self.get_info(obj) for obj in self.board[key]] for key in self.board}
        for player in self.players:
            player.strategy.simple_board = simple_board

    def translate(self, x,y):
        x1, x2 = x
        y1, y2 = y
        return (x1+y1, x2+y2)
    
    def enemy_in_coord(self, obj):
        coord = obj.coords
        for item in self.board[coord]:
            if item.player_num != obj.player_num:
                if coord not in self.combat_coords and isinstance(obj, Ship) and isinstance(item, Ship):
                    self.combat_coords.append(coord)
                return True
        return False
    
    def move(self, ship, translation):
        new_coords = self.translate(ship.coords, translation)
        self.logs.write('\tMOVING PLAYER '+str(ship.player_num)+' '+str(ship.name)+' '+str(ship.ship_num)+': '+str(ship.coords)+' -> '+str(new_coords)+'\n')
        self.delete(ship)
        ship.update_coords(new_coords)
        self.add(ship)
    
    def complete_move_phase(self):
        if self.winner != None:
            return
        self.logs.write('START TURN '+str(self.turn)+' MOVEMENT PHASE\n\n')
        for player in self.players:
            if len(player.ships) == 0:
                self.logs.write('PLAYER '+str(player.player_num)+' HAS NO SHIPS\n\n')
                continue
            self.logs.write('PLAYER '+str(player.player_num)+' MOVING:\n')
            for ship in player.ships:
                if self.enemy_in_coord(ship):
                    continue
                ship_info = self.get_info(ship)
                choices = self.get_in_bounds_translations(ship_info['coords'])
                move = player.choose_translation(ship_info, choices)
                if move not in choices:
                    self.logs.write('INVALID CHOICE\n')
                    print('invalid move')
                    continue
                self.move(ship, move)
                self.enemy_in_coord(ship)
                self.update_simple_boards()
            self.logs.write('\n')
        self.logs.write('END TURN '+str(self.turn)+' MOVEMENT PHASE\n\n')
    
    def roll(self):
        return random.randint(1,10)
    
    def hit(self, attacker, defender):
        if attacker.hp <= 0 or defender.hp <= 0:
            self.logs.write('ATTEMPTED COMBAT WITH DEAD SHIP - ATTEMPT STOPPED\n')
            print('ATTEMPTED COMBAT WITH DEAD SHIP')
            return None
        if attacker.player_num == defender.player_num:
            self.logs.write('ATTEMPT TO ATTACK OWN SHIP - ATTEMPT STOPPED\n')
            print('ATTEMPTED TO ATTACK OWN SHIP')
            return None
        roll = self.roll()
        new_atk = attacker.atk - defender.df
        self.logs.write('\tPLAYER '+str(attacker.player_num)+' '+str(attacker.name)+' '+str(attacker.ship_num)+' ATTACKING PLAYER '+str(defender.player_num)+' '+str(defender.name)+' '+str(defender.ship_num)+'...')
        if roll <= new_atk:
            self.logs.write('HIT!\n')
            return True
        self.logs.write('MISS\n')
        return False
    
    def remove_ship(self, ship):
        player = self.players[ship.player_num - 1]
        player.ships.remove(ship)
        self.delete(ship)

    def get_enemies(self, ship, combat_list):
        return [obj for obj in combat_list if obj.player_num != ship.player_num and obj.hp > 0]
    
    def all_same_team(self, ship_list):
        return len(set([ship.player_num for ship in ship_list])) == 1
    
    def check_if_on_board(self, obj): # for debugging
        for key in self.board:
            if obj in self.board[key]:
                return True
        return False
    
    def objs_to_info(self, obj_list):
        if type(obj_list) != list:
            obj_list = [obj_list]
        return [self.get_info(obj) for obj in obj_list]
    
    def obj_from_info(self, info):
        for item in self.board[info['coords']]:
            if item.__dict__ == info:
                return item

    def complete_combat_phase(self): # prioritization: class, tactics, first in coord
        if self.winner != None:
            return
        self.logs.write('START TURN '+str(self.turn)+' COMBAT PHASE\n\n')
        ended_combat = []
        for coord in self.combat_coords:
            self.logs.write('COMBAT AT '+str(coord)+':\n\n')
            by_cls = sorted(self.all_ships(coord), key=lambda x: x.ship_class)
            # by tactics (not yet available)
            # by chronological order is already built-in via appending
            self.logs.write('\tCOMBAT ORDER:\n')
            for ship in by_cls:
                self.logs.write('\t\tPLAYER '+str(ship.player_num)+' '+str(ship.name)+' '+str(ship.ship_num)+'\n')
            self.logs.write('\n\tBEGINNING COMBAT...\n\n')
            for ship in by_cls:
                if ship.hp <= 0:
                    continue
                player = self.players[ship.player_num - 1]
                combat_order = [self.get_info(obj) for obj in by_cls if obj.hp > 0]
                enemies = self.get_enemies(ship, by_cls)
                if len(enemies)==0:
                    continue
                target_info = player.choose_target(self.get_info(ship), combat_order)
                target = self.obj_from_info(target_info)
                if target not in enemies:
                    self.logs.write('TARGET NOT VALID - COMBAT ATTEMPT STOPPED\n')
                    print('invalid target')
                    continue
                if self.hit(ship, target):
                    target.hp -= 1
                    if target.hp <= 0:
                        self.logs.write('\tPLAYER '+str(target.player_num)+' '+str(target.name)+' '+str(target.ship_num)+' WAS DESTROYED IN COMBAT\n')
                        self.remove_ship(target)
                self.update_simple_boards()
            by_cls = [ship for ship in by_cls if ship.hp > 0]
            if self.all_same_team(by_cls) or len(by_cls)==0:
                ended_combat.append(coord)
            self.logs.write('\n')
        self.combat_coords = [coord for coord in self.combat_coords if coord not in ended_combat]
        self.logs.write('END TURN '+str(self.turn)+' COMBAT PHASE\n\n')
        self.turn += 1
    
    def remove_player(self, player):
        for ship in player.ships:
            self.remove_ship(ship)
        for col in player.colonies:
            self.delete(col.coords)
        self.players.remove(player)
        self.delete(player.home_col)
    
    def check_for_winner(self):
        for player in self.players:
            if self.enemy_in_coord(player.home_col):
                self.logs.write('PLAYER '+str(player.player_num)+' HAS BEEN REMOVED FROM THE GAME\n\n')
                self.remove_player(player)
        if len(self.players) == 1:
            self.winner = self.players[0].player_num
            self.logs.write('PLAYER '+str(self.winner)+' HAS WON')
        if len(self.players) == 0:
            self.logs.write('IT IS A TIE')
            self.winner = "Tie"
    
    def run_to_completion(self):
        while self.winner == None:
            
            self.complete_move_phase()
            self.complete_combat_phase()
            self.check_for_winner()
    
    def play_n_turns(self, n):
        for _ in range(n):
            self.complete_move_phase()
            self.complete_combat_phase()
            self.check_for_winner()
