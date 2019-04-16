from playing.utils.framework import Player


# Class for the human player
class HumanPlayer(Player):

    # Don't need any properties for the Human player
    def __init__(self):
        pass

    # Define the move the player makes
    def move(self, game):
        # Get all the possible moves
        moves = game.moves()
        # Print all the possible moves
        print("Possible moves:", moves)

        # Initialize the move
        move = None

        # Run until we are given a legal move
        while move not in moves:
            # Save the move
            move = eval(input("Your choice: "))

        # Return the move
        return move
