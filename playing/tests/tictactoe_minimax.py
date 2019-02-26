from playing.games.tictactoe import TicTacToe
from playing.players.minimax import MaxPlayer, MinPlayer

max_player = MaxPlayer()
min_player = MinPlayer()

max_player.assume(min_player)
min_player.assume(max_player)

game = TicTacToe()
game.play(max_player, min_player)