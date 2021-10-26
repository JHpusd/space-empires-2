import sys
sys.path[0] = '/workspace/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from move_off import *

players = [Player(MoveToClosestCol()), Player(MoveOff())]
game = Game(players, log_name='test_move_off_tests.txt')

game.run_to_completion()
print(game.winner)
