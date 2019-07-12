# Author: Tomas Cespedes
from collections import deque
from math import inf

import sys

from LightsOutPuzzle.utils.framework import Agent

NOT_FOUND = None


class IterativeAStarAgent(Agent):

    def __init__(self):
        self.moves = list()

    # Return the move this agent wants to make
    def move(self, puzzle):
        # Plan a move if necessary
        if not self.moves:
            self.moves = self.iterative_deepening_search(puzzle)

        return self.moves.popleft()

    def iterative_deepening_search(self, puzzle):
        """
        Run iterative deepening search combined with A-star.
        :param puzzle: a puzzle in some state.
        :return: a result which is our ideal move if successful, otherwise None.
        """
        threshold = puzzle.heuristic()
        path = deque()

        # Do this until we hit the threshold
        for depth in range(sys.maxsize ** 2):
            # Get our new result
            result = self.recursive_dls(path, puzzle, 0, threshold)
            # Check if our result is a deque
            if isinstance(result, deque):
                # If so, this is our answer
                return result
            # Check if it is infinity (means no answer)
            if result == inf:
                return NOT_FOUND
            # update the threshold
            threshold = result

    def recursive_dls(self, moves_list, puzzle, current_node_cost,  threshold):
        """
        :param moves_list: a list of moves
        :param puzzle: a puzzle in some state
        :param current_node_cost: the cost it takes to get to current node
        :param threshold: a limit in which our puzzle should not go past.
        :return: Cost if it is greater than our threshold, a list of moves if
        our agent is successful, minimum if we fail, or a result if our agent is still
        trying to solve the puzzle.
        """
        # Update the cost
        cost = current_node_cost + puzzle.heuristic()

        # If our cost is greater than our threshold
        if cost > threshold:
            # Return our
            return cost

        # If the puzzle is solved
        # Check if this puzzle is our solution
        if puzzle.solved():
            # return list of moves
            return moves_list

        # Set the minimum value
        minimum = inf
        # Go through all the possible moves
        for move in puzzle.moves():
            # check if move is already in list
            if move not in moves_list:
                # Append the move
                moves_list.append(move)
                # Get the neighbor of the puzzle
                child = puzzle.neighbor(move)
                # Get the new result
                result = self.recursive_dls(moves_list, child, current_node_cost + 1, threshold)

                # Check if the result is a deque
                if isinstance(result, deque):
                    # This is our answer
                    return result
                # If the result is less than the minimum value
                if result < minimum:
                    # Update our new minimum
                    minimum = result

                # If we get here, get rid of the move
                moves_list.pop()

        # Failed
        return minimum
