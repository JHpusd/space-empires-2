import math, random, sys
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

        global board_x, board_y, mid_x, mid_y
        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2
        self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]

        self.turn = 1
        self.winner = None

        self.set_up_game()
    
    def set_player_numbers(self):
        for i,player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.state['board_size']
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.state['board_size']
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
    
    def add_to_coord(self, objs, coord):
        for obj in objs:
            self.board[coord[1]][coord[0]].append(obj)
    
    def set_up_game(self):
        starts = [(0, mid_x-1), (board_y-1, mid_x-1), (mid_y-1, 0), (mid_y-1, board_x-1)]
        for i in range(len(self.players)):
            player = self.players[i]
            player_num = self.players[i].player_number
            coord = starts[i]

            player.set_home_col(coord)
            self.add_to_coord([player.home_col], coord)
            for _ in range(3): # need to change if number of initial ships changes
                scout = Scout(player_num, coord)
                bc = BattleCruiser(player_num, coord)
                self.add_to_coord([scout, bc], coord)
                player.add_ships([scout, bc])
