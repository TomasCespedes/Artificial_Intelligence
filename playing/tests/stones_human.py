from random import randint
from playing.games.stones import Stones
from playing.players.human import HumanPlayer

max_player = HumanPlayer(True)
min_player = HumanPlayer(False)

game = Stones(10)
game.play(max_player, min_player, 0)
