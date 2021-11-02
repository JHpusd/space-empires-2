import sys
sys.path[0] = '/workspace/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from pause_strat import *
from cayden import *
from maia import *
from anton import *
from william import *
from charlie import *

#players = [Player(MoveToClosestCol()) for _ in range(2)]
players = [Player(MoveToClosestCol()), Player(AntonStrat())]
game = Game(players, log_name='ver_1_logs.txt')

game.run_to_completion()
print(game.winner)