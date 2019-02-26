# Author: Tomas Cespedes
# Citations: None
# Collaboration: Taylor Digilio and Cooper Parker

import random
from solving.utils.framework import Agent
from math import exp


class SimulatedAnnealingAgent(Agent):
    def __init__(self, start=1.0, stop=0.001, decay=0.999):
        # Initialize all variables
        self.moves = set()
        self.tempature = start
        self.stop = stop
        self.decay = decay

    def move(self, puzzle):
        # Plan a move if necessary
        if puzzle not in self.moves:
            self.anneal(puzzle)

        # Return the possible moves of that puzzle
        return self.moves[puzzle]

    def anneal(self, puzzle):
        while self.tempature > self.stop:

            # Copy over the moves to current puzzle from the new puzzle
            for move in puzzle.moves():
                self.moves.add(move)

            # Randomly choose a move from the set
            random_move = random.choice(tuple(self.moves))
            # Get that move's neighbor
            random_neighbor = puzzle.neighbor(random_move)
            # Get the move's neighbor's heuristic value
            random_neighborvalue = random_neighbor.heuristic()

            # Check if the puzzle is solved
            if puzzle.solved():
                print("Success")
                quit()

            # If not solved, check if neighbor's heuristic value is
            # less than the puzzle's current heuristic value
            elif random_neighborvalue < puzzle.heuristic() or exp(
                    (puzzle.heuristic() - random_neighborvalue) / self.tempature):

                # Neighbor puzzle is better so make the new puzzle the neighbor puzzle
                puzzle = random_neighbor
                # Change the tempature for annealing method
                self.tempature *= self.decay
                # Display the puzzle
                puzzle.display()

        # If you get here, the search has failed
        print("Failure!!")
        quit()

