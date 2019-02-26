# Author: Tomas Cespedes
# Citations: None
# Collaboration: Taylor Digilio and Cooper Parker

from playing.utils.framework import Game
from copy import deepcopy

SIZE = 3

TICTACTOE = [
     "123",
     "456",
     "789"
    ]


class TicTacToe(Game):
    def __init__(self, tictactoe=TICTACTOE, last_player=None, last_move=None):
        self.tictactoe = tictactoe
        self.last_player = last_player
        self.last_move = last_move

    def __eq__(self, other):
        return self.tictactoe == other

    def __hash__(self):
        return hash(str(self.tictactoe))

    # Determine where the game is at any point
    # Return None (game is still playing), -1 (Max player won),
    # +1 (Min player won), or 0 (There has been a draw)
    def utility(self):

        # Check to see if any three symbols in a row match
        if (self.tictactoe[0][0] == self.tictactoe[0][1] and self.tictactoe[0][1] == self.tictactoe[0][2]) or \
            (self.tictactoe[0][0] == self.tictactoe[1][0] and self.tictactoe[1][0] == self.tictactoe[2][0]) or \
            (self.tictactoe[0][0] == self.tictactoe[1][1] and self.tictactoe[1][1] == self.tictactoe[2][2]) or \
            (self.tictactoe[0][1] == self.tictactoe[1][1] and self.tictactoe[1][1] == self.tictactoe[2][1]) or \
            (self.tictactoe[0][2] == self.tictactoe[1][2] and self.tictactoe[1][2] == self.tictactoe[2][2]) or \
            (self.tictactoe[1][0] == self.tictactoe[1][1] and self.tictactoe[1][1] == self.tictactoe[1][2]) or \
            (self.tictactoe[2][0] == self.tictactoe[2][1] and self.tictactoe[2][1] == self.tictactoe[2][2]) or \
                (self.tictactoe[2][0] == self.tictactoe[1][1] and self.tictactoe[2][0] == self.tictactoe[0][2]):

            # Check who went last if someone won
            if self.last_player.maximizes():
                return 1
            else:
                return -1

        # If there are still digits left (open spots),
        # Return None to continue the game.
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tictactoe[i][j].isdigit():
                    return None

        # Otherwise, there has been a tie so return 0.
        return 0

    # Create a list of possible moves
    def moves(self):
        moves = list()

        # If go through the board
        for r in range(SIZE):
            for c in range(SIZE):
                # If there is a digit (open space)
                # Append the move to the list
                if self.tictactoe[r][c].isdigit():
                    moves.append((r, c))

        # Return list of moves
        return moves

    # Create a possible child of the game
    def child(self, move, player):
        # Break apart the move
        (r, c) = move

        # Deep copy the board
        newgrid = deepcopy(self.tictactoe)

        # Create a placeholder for the line
        line = ""

        # If Max Player went, draw an X
        if player.maximizes():
            for i in range(len(newgrid[r])):
                if i == c:
                    line += "X"
                else:
                    line += newgrid[r][i]

        # Min player went, draw an O
        else:
            for i in range(len(newgrid[r])):
                if i == c:
                    line += "O"
                else:
                    line += newgrid[r][i]

        # Save the updated row
        newgrid[r] = line

        # Return new object
        return TicTacToe(newgrid, player, move)

    # Display the board
    def display(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.tictactoe[r][c].isdigit():
                    print("_", end='')
                else:
                    print(self.tictactoe[r][c], end='')
            print()
        print()





