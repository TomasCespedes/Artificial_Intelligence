# Author: Tomas Cespedes
# Citations: None
# Collaboration: Taylor Digilio and Cooper Parker

from playing.utils.framework import Player
from math import inf


# Intermediate superclass for MIN and MAX
class MiniMaxPlayer(Player):

    def __init__(self):
        self.moves = dict()
        self.values = dict()
        self.opponent = None

    # Real opponent if possible - otherwise an imaginary one
    def assume(self, opponent):
        self.opponent = opponent

    # Return whether this player wants to maximize utility
    def maximizes(self):
        raise NotImplementedError

    # Return the move this player wants to make
    def move(self, game):
        if game not in self.moves:
            self.value(game, -inf, +inf)
        return self.moves[game]

    # Return the best future utility this player can achieve
    def value(self, game, alpha, beta):
        raise NotImplementedError


class MaxPlayer(MiniMaxPlayer):

    # Return whether this player wants to maximize utility
    def maximizes(self):
        return True

    # Return the MAX future utility this player can achieve
    def value(self, game, alpha=-inf, beta=+inf):
        if game not in self.values:

            # Check if the game is over
            utility = game.utility()
            if utility is not None:
                return utility

            # Set value to -infinity
            self.values[game] = -inf

            # For every move possible
            for move in game.moves():

                # For the child of that move
                child = game.child(move, self)

                # Get the value of that child
                child_value = self.opponent.value(child, alpha, beta)

                # If new value is bigger than old value,
                # Update the value and save the move
                if child_value > self.values[game]:
                    self.values[game] = child_value
                    self.moves[game] = move

                # If new value is bigger than alpha,
                # update alpha
                if self.values[game] > alpha:
                    alpha = self.values[game]

                # If beta is less than alpha, break
                if beta <= alpha:
                    break

                # Regular Min_max
                # child = game.child(move, self)
                # child_value = self.opponent.value(child)
                #
                # if child_value > self.values[game]:
                #     self.values[game] = child_value
                #     self.moves[game] = move

        # Return the new value
        return self.values[game]


class MinPlayer(MiniMaxPlayer):
    # Return whether this player wants to maximize utility
    def maximizes(self):
        return False

    # Return the MIN future utility this player can achieve
    def value(self, game, alpha=-inf, beta=+inf):
        if game not in self.values:

            # Check if the game is over
            utility = game.utility()
            if utility is not None:
                return utility

            # Set value to + infinity
            self.values[game] = +inf

            # For every move available
            for move in game.moves():

                # With alpha-beta pruning Min_max

                # Get the child of the game
                child = game.child(move, self)

                # Get the child's value
                child_value = self.opponent.value(child, alpha, beta)

                # If the child value is less than current value
                if child_value < self.values[game]:
                    # Set the new value to the child value
                    self.values[game] = child_value
                    # Save the new move
                    self.moves[game] = move

                # If the value is less than beta,
                # update beta
                if self.values[game] < beta:
                    beta = self.values[game]

                # If beta is less than alpha then break
                if beta < alpha:
                    break

                # Regular Min_max
                # self.values[game] = min(self.values[game], child_value)
                # beta = min(beta, self.values[game])
                # if beta <= alpha:
                #     break

        # Return the value
        return self.values[game]
