import sys
sys.path[0] = '/workspace/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from pause_strat import *
from custom_strat import *

players = [Player(CompetitionStrat()), Player(CompetitionStrat())]
game = Game(players, log_name='econ_test.txt')
game.run_to_completion()