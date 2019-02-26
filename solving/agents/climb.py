# Author: Tomas Cespedes
# Citations: None
# Collaboration: Taylor Digilio and Cooper Parker

from solving.utils.framework import Agent, Puzzle

class HillClimbingAgent(Agent):

    def __init__(self):
        self.moves = dict()

    def move(self, puzzle):
        # Plan a move if necessary
        if puzzle not in self.moves:
            self.climb(puzzle)

        return self.moves[puzzle]

    def climb(self, puzzle):
        small = puzzle.heuristic()
        smallest = puzzle

        for move in puzzle.moves():
            if puzzle.neighbor(move).heuristic() < small:
                small = puzzle.neighbor(move).heuristic()
                smallest = puzzle.neighbor(move)

        if smallest.solved():
            print("Success :)")
            quit()
        elif smallest.heuristic() >= puzzle.heuristic():
            print("Failure :(")
            quit()

        puzzle = smallest
        puzzle.display()

        self.climb(puzzle)