from LightsOutPuzzle.puzzles.lightsout import Lightsout
from LightsOutPuzzle.agents.human import HumanPlayer

# Initialize the human player
player = HumanPlayer()
# Initialize the game
game = Lightsout()
# Allow the user to play the game
game.play(player)