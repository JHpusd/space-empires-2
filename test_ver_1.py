import sys
sys.path.append('ver_1')
from game import *
from players import *

players = [CustomPlayer() for _ in range(2)]
game = Game(players)

def print_state():
    for player in game.players:
        print("Player {}\'s pieces:".format(player.player_number))
        print("Home colony coords:", player.home_col.coords)
        for ship in player.ships:
            print(ship.name+":", ship.coords)
        print("\n")

print_state()
print("move 1\n")
game.complete_move_phase()
print_state()