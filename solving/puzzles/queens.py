from solving.utils.framework import Puzzle

SIZE = 8

START = list(range(SIZE))


class Queens(Puzzle):

    def __init__(self, columns=START):
        self.columns = columns

    # Return whether this puzzle is equivalent to the other
    def __eq__(self, other):
        return self.columns == other.columns

    # Return a hash code for this puzzle
    def __hash__(self):
        return hash(str(self.columns))

    # Return whether this puzzle comes before the other in a sort
    def __lt__(self, other):
        return self.columns < other.columns

    # Return whether this puzzle is solved
    def solved(self):
        return self.heuristic() == 0

    # Return an estimate of how far this puzzle is from being solved
    def heuristic(self):
        conflicts = 0
        for r1 in range(SIZE):
            c1 = self.columns[r1]
            for r2 in range(r1 + 1, SIZE):
                c2 = self.columns[r2]
                if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    conflicts += 1
        return conflicts

    # Return a list of legal moves
    def moves(self):
        moves = list()
        for r in range(SIZE):
            for c in range(SIZE):
                if c != self.columns[r]:
                    moves.append((r, c))
        return moves

    # Return a new puzzle created by a move
    def neighbor(self, move):
        (r, c) = move
        new_columns = self.columns.copy()
        new_columns[r] = c
        return Queens(new_columns)

    # Print this puzzle to the console
    def display(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.columns[r] == c:
                    print('Q', end=' ')
                else:
                    print('Ø', end=' ')
            print()
        print()
