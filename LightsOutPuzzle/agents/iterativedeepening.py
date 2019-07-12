# Author: Tomas Cespedes
from collections import deque
from LightsOutPuzzle.utils.framework import Agent


class IterativeDeepeningAgent(Agent):

    def __init__(self):
        self.moves = list()
        self.cutoff = 50

    # Return the move this agent wants to make
    def move(self, puzzle):
        """
        Plan the move the agent wants to make.
        :param puzzle: a puzzle in some state.
        :return: the left most move (the best move to make)
        """
        # Plan a move if necessary
        if not self.moves:
            self.moves = self.iterative_deepening_search(puzzle)
        return self.moves.popleft()

    def iterative_deepening_search(self, puzzle):
        """
        Calls recursive depth limited search to convert to iterative deepening search.
        :param puzzle: a puzzle in some state.
        :return: result if we find a solution, otherwise None.
        """
        for depth in range(self.cutoff):
            result = self.recursive_dls(deque(), puzzle, depth)
            if result != self.cutoff:
                return result
        return None

    def recursive_dls(self, moves_list, puzzle, limit):
        """
        :param moves_list: a list of all possible moves.
        :param puzzle: a puzzle in whichever state it is currently in.
        :param limit:  a limit in which the user stops at.
        :return: Ideally, a result in which the planned move is better than previous move. If puzzle is solved,
        we return the moves list that gets us the best result.
        """
        # If the puzzle is solved
        if puzzle.solved():
            # return list of moves
            return moves_list

        # If limit is 0
        # return the cutoff
        elif limit == 0:
            # return cutoff
            return self.cutoff

        else:
            # Cutoff has not occured
            cutoff_occured = False

            # Go through all the possible moves
            for move in puzzle.moves():

                if move not in moves_list:
                    moves_list.append(move)

                    # Get the neighbor of the puzzle
                    child = puzzle.neighbor(move)

                    result = self.recursive_dls(moves_list, child, limit - 1)

                    # Result is equal to the cutoff so
                    # remove the move in put into the list
                    if result == self.cutoff:
                        moves_list.pop()
                        cutoff_occured = True

                    # If result is not None (None means we failed)
                    elif result is not None:
                        return result

                    else:
                        moves_list.pop()

            if cutoff_occured:
                return self.cutoff
            else:
                return None




