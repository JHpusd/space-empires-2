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


winners = {1:0, 2:0, 'Tie':0}
players = [Player(CompetitionStrat()), Player(MaiaComp())]
for _ in range(50):
    game = Game(players, log_name='comp_first_half.txt')
    game.run_to_completion()
    winners[game.winner] += 1
print(winners)

winners = {1:0, 2:0, 'Tie':0}
players = [Player(MaiaComp()), Player(CompetitionStrat())]
for _ in range(50):
    game = Game(players, log_name='comp_second_half.txt')
    game.run_to_completion()
    winners[game.winner] += 1
print(winners)

# justin vs william: 76:24
# justin vs charlie: 64:36
# maia vs cayden: 22:78
# maia vs anton: 43:57
# maia vs william: 49:51
# maia vs charlie: 50:50
# cayden vs anton: 58:42
# cayden vs william: 70:30
# cayden vs charlie: 71:29
# anton vs william: 63:37
# anton vs charlie: 56:44
# william vs charlie: 57:43