from solving.utils.framework import Puzzle

SIZE = 20

EXIT = (SIZE - 2, SIZE - 1)

GRID = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X     X    X       X",
    "X XXXXX XXXX XXX XXX",
    "X       X      X X X",
    "X X XXX XXXXXX X X X",
    "X X   X        X X X",
    "X XXX XXXXXX XXXXX X",
    "X XXX    X X X     X",
    "X    XXX       XXXXX",
    "XXXXX   XXXXXX     X",
    "X   XXX X X    X X X",
    "XXX XXX X X XXXX X X",
    "X     X X   XX X X X",
    "XXXXX     XXXX X XXX",
    "X     X XXX    X   X",
    "X XXXXX X XXXX XXX X",
    "X X     X  X X     X",
    "X X XXXXXX X XXXXX X",
    "X X                 ",
    "XXXXXXXXXXXXXXXXXXXX"
]

class Maze(Puzzle):
    def __init__(self, row=1, column=1):
        self.row = row
        self.column = column

    # Compare equality between two puzzles
    def __eq__(self, other):
        return (self.row, self.column) == (other.row, other.column)

    # Hash the puzzle since we are using eq
    def __hash__(self):
        return hash((self.row, self.column))

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    # Return an estimate of how far this puzzle is from being solved
    def heuristic(self):
        conflicts = abs(self.row - EXIT[0]) + abs(self.column - EXIT[1])
        return conflicts

    # Return whether a puzzle is solved
    def solved(self):
        # Returns true if the position of agent is equal to Exit position
        return (self.row, self.column) == EXIT

    # Return a list of legal moves
    def moves(self):
        moves = list()

        # Check all the possible moves and see if theres an X there.
        # If there is not an X, it is a legal move.
        # Up
        if GRID[self.row - 1][self.column] != 'X':
            moves.append((-1, 0))
        # Down
        if GRID[self.row + 1][self.column] != 'X':
            moves.append((+1, 0))
        # Left
        if GRID[self.row][self.column - 1] != 'X':
            moves.append((0, -1))
        # Right
        if GRID[self.row][self.column + 1] != 'X':
            moves.append((0, +1))

        return moves

    # Return a new puzzle created by a move
    def neighbor(self, move):
        (dr, dc) = move
        return Maze(self.row + dr, self.column + dc)


    # Print this puzzle to the console
    def display(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if (r, c) == (self.row , self.column):
                    print('*', end='')
                else:
                    print(GRID[r][c], end='')
            print()
        print()



