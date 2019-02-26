# Author: Tomas Cespedes
# Citations: None
# Worked with: Taylor Digilio and Cooper Parker
# Date: 1/28/19


from solving.utils.framework import Puzzle

SIZE = 5

EXIT = [
    "XXXXX",
    "X123X",
    "X456X",
    "X78 X",
    "XXXXX"
]

TILES = [
    "XXXXX",
    "X867X",
    "X254X",
    "X3 1X",
    "XXXXX"
]

class Tiles(Puzzle):
    def __init__(self, grid=TILES, row=3, column=2):
        self.grid = grid
        self.row = row
        self.column = column

    # Compare equality between two puzzles
    def __eq__(self, other):
        return self.grid == other

    # Hash the puzzle since we are using eq
    def __hash__(self):
        return hash(str(self.grid))

    def heuristic(self):
        conflicts = 0
        for r in range(SIZE):
            for c in range(SIZE):
                if self.grid[r][c] != EXIT[r][c]:
                    for row in range(SIZE):
                        for col in range(SIZE):
                            if self.grid[row][col] == EXIT[r][c]:
                                conflicts += (abs(row - r) + abs(col - c))

        return conflicts

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    # Return whether a puzzle is solved
    def solved(self):
        return self.grid == EXIT

    # Return a list of legal moves
    def moves(self):
        moves = list()

        # Left
        if self.grid[self.row - 1][self.column] != "X":
            moves.append((-1, 0))
        # Right
        if self.grid[self.row + 1][self.column] != "X":
            moves.append((+1, 0))
        # Up
        if self.grid[self.row][self.column - 1] != "X":
            moves.append((0, -1))
        # Down
        if self.grid[self.row][self.column + 1] != "X":
            moves.append((0, +1))

        return moves

    # Return a new puzzle created by a move
    def neighbor(self, move):
        (dr, dc) = move
        new_tilespot = self.grid[self.row + dr][self.column + dc]
        new_tiles = self.grid.copy()

        # Line for current row
        line = ""

        # Check all the items in the current row
        # and recreate the row
        # Since we are tracking empty spot, this will always change
        for item in new_tiles[self.row]:
            # Current item is equal to where blank spot should be
            if item == new_tilespot:
                line += " "
            # If current item is blank, replace with a new item
            elif item == " ":
                line += new_tilespot
            # Otherwise, just copy the original item
            else:
                line += item

        # Add new line back into the Tiles
        new_tiles[self.row] = line

        # If another row changes that is not the current one
        # Recreate the line with the new tiles
        if self.row != self.row + dr:
            # Line for new row
            line2 = ""
            for item in new_tiles[self.row + dr]:
                if item == new_tilespot:
                    line2 += " "
                else:
                    line2 += item

            # Add new line back into the Tiles
            new_tiles[self.row + dr] = line2

        return Tiles(new_tiles, self.row + dr, self.column + dc)

    # Print this puzzle to the console
    def display(self):
        for r in range(SIZE):
            for c in range(SIZE):
                # If spot is the current empty tile (print empty tile)
                if (r, c) == (self.row, self.column):
                    print(' ', end='')
                # Otherwise, print the tile
                else:
                    print(self.grid[r][c], end='')
            print()
        print()



