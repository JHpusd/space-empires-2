import sys
sys.path[0] = '/workspace/space-empires-2'
from game import *
from player import *
sys.path.append('strategies')
from move_strat import *
from pause_strat import *
from custom_strat import *
from cayden import *
from maia import *
from anton import *
from william import *
from charlie import *
from dummy_strat import *


winners = {1:0, 2:0, 'Tie':0}
players = [Player(CompetitionStrat()), Player(CaydenStrat())]
for _ in range(50):
    game = Game(players, log_name='comp_first_half.txt')
    game.run_to_completion()
    winners[game.winner] += 1
print(winners)

winners = {1:0, 2:0, 'Tie':0}
players = [Player(CaydenStrat()), Player(CompetitionStrat())]
for _ in range(50):
    game = Game(players, log_name='comp_second_half.txt')
    game.run_to_completion()
    winners[game.winner] += 1
print(winners)

