# Author: Tomas Cespedes
# Worked with: Taylor Digilio and Cooper Parker
# Date: 2/4/19

from solving.utils.framework import Agent
from solving.utils.structures import PriorityQueue, SearchTree


class AStarAgent(Agent):

    def __init__(self):
        self.moves = dict()

    # Return the move this agent wants to make
    def move(self, puzzle):

        # Plan a move if necessary
        if puzzle not in self.moves:
            self.astar(puzzle)

        return self.moves[puzzle]

    # Use breadth-first search to plan moves
    def astar(self, puzzle):

        tree = SearchTree(puzzle)

        finalized = set()

        frontier = PriorityQueue()
        frontier.push(puzzle, puzzle.heuristic())

        while len(frontier) > 0:
            # remove the oldest thing from the queue
            leaf = frontier.pop()
            # Add leaf to the finalized set
            finalized.add(leaf)

            if leaf.solved():
                self.moves = tree.branch(leaf)
                return

            # look through the list of moves 1 by 1
            for move in leaf.moves():
                neighbor = leaf.neighbor(move)
                if neighbor not in finalized:
                    if neighbor not in tree:
                        tree.connect(neighbor, leaf, move)
                        frontier.push(neighbor, tree.depth(neighbor)
                                      + neighbor.heuristic())

                    if tree.depth(leaf) + 1 < tree.depth(neighbor):
                        tree.connect(neighbor, leaf, move)
                        frontier.prioritize(neighbor, tree.depth(neighbor)
                                            + neighbor.heuristic())

        print("Failed :(")
        quit()