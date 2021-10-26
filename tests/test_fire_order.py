import sys
sys.path[0] = '/workspace/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from pause_strat import *

players = [Player(PauseStrat()), Player(MoveToClosestCol())]
game = Game(players, log_name='test_combat_order_tests.txt')

game.run_to_completion()
print(game.winner)
