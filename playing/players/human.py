from playing.utils.framework import Player


class HumanPlayer(Player):

    def __init__(self, maximize):
        self.maximize = maximize

    def maximizes(self):
        return self.maximize

    def move(self, game):
        moves = game.moves()
        print("Possible moves:", moves)

        move = None
        while move not in moves:
            move = eval(input("Your choice: "))
        return move
