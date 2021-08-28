import sys
sys.path.append('ver_1')
from game import *
from players import *

players = [CustomPlayer() for _ in range(2)]
game = Game(players)