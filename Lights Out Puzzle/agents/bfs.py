from solving.utils.framework import Agent
from solving.utils.structures import Queue, SearchTree


class BFSAgent(Agent):

    def __init__(self):
        self.moves = dict()

    def move(self, puzzle):

        # Plan a move if necessary
        if puzzle not in self.moves:
            self.bfs(puzzle)

        return self.moves[puzzle]

    # Use Breadth First Search to plan moves
    def bfs(self, puzzle):

        tree = SearchTree(puzzle)

        frontier = Queue()
        frontier.push(puzzle)

        while len(frontier) > 0:
            leaf = frontier.pop()
            for move in leaf.moves():
                neighbor = leaf.neighbor(move)
                if neighbor not in tree:
                    tree.connect(neighbor, leaf, move)
                    frontier.push(neighbor)

                    if neighbor.solved():
                        self.moves = tree.branch(neighbor)
                        return
        print("Failed :(")
        quit()
