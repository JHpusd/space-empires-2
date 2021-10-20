import sys
sys.path[0] = '/home/runner/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from pause_strat import *
from cayden import *

players = [Player(MoveToClosestCol()) for _ in range(2)]
game = Game(players, log_name='ver_1_logs.txt')

game.run_to_completion()
print(game.winner)