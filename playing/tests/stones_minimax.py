from time import sleep

from playing.games.stones import Stones
from playing.players.minimax import MaxPlayer, MinPlayer

max_player = MaxPlayer()
min_player = MinPlayer()

max_player.assume(min_player)
min_player.assume(max_player)

game = Stones(5)
game.play(max_player, min_player)
