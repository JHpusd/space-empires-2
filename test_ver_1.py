import sys
sys.path.append('ver_1')
from game import *
from player import *
from strategy import *

players = [Player(MoveToClosestCol()) for _ in range(2)]
game = Game(players, log_name='ver_1_logs.txt')

game.run_to_completion()
print(game.winner)