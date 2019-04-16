from collections import deque
from LightsOutPuzzle.utils.framework import Puzzle
from copy import deepcopy

# Set up the game board size
SIZE = 5

SOLVEABLE_BOARDS = [
    # Board 1 (8 moves)
    [
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1]
    ],
    # Board 2 (Ideally 10 but 12 moves)
    [
        [0, 1, 0, 1, 1],
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 1, 1, 1, 1]
    ],
    # Board 3 (12 moves)
    [
        [0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1],
        [1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 1, 1]
    ],
    # Board 4 (5 moves)
    [
        [0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 1, 1, 1]
    ],
    # Board 5 (5 moves)
    [
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 1]
    ]
]

# Set up the game board
LIGHTSOUT = SOLVEABLE_BOARDS[0]

# Can create the moves list once here
# To save time since the moves list never changes
MOVES = list()
for i in range(SIZE):
    for j in range(SIZE):
        # Append every possible move
        MOVES.append((i, j))


class Lightsout(Puzzle):

    # Constructor
    def __init__(self, grid=LIGHTSOUT):
        self.grid = grid

    # Games are equal if grids are equal
    def __eq__(self, other):
        return self.grid == other.grid

    # Hash the grid
    def __hash__(self):
        return hash(str(self.grid))

    # Heuristic compare makes this easy
    def __lt__(self, other):
        return self.grid < other.grid

    # Game is done when our conflicts equal 0
    def solved(self):
        return self.heuristic() == 0

    # The tiles that are 1's (light up) are a conflict.
    def heuristic(self):
        # Initialize conflict counter
        conflicts = 0

        # Go through every cell
        for (dr, dc) in MOVES:
            if self.grid[dr][dc] == 1:
                conflicts += 1

        # Worst case is 12 moves so cap it
        # Add this only for iterative deepening a*
        # This is to limit the number of conflicts since the max
        # Number of moves is 12 (not best solution but solves our issue)
        # Need a different heuristic to solve the issue which calculates number of moves
        #if conflicts >= 13:
        #    conflicts = 12

        return conflicts

    # Every coordinate is a possible move
    def moves(self):
        # Return the list of moves
        return MOVES

    def neighbor(self, move):
        # Get the row number and column number from the move
        (dr, dc) = move

        # Deep copy a new grid
        new_grid = deepcopy(self.grid)

        # Update the new grid with new move
        self.switch(new_grid, dr, dc)

        # Pass the new grid with a new object
        return Lightsout(new_grid)

    # Function to make the appropriate move
    # It changes the clicked spot and its neighbors
    # 0 ^= 1  turns a 0 into a 1
    # 1 ^= 1 turns a 1 into a 0
    def switch(self, new_grid, dr, dc):
        # Switch the current spot
        new_grid[dr][dc] ^= 1

        # Check if there is something to switch one row above
        if (dr - 1) >= 0:
            new_grid[dr - 1][dc] ^= 1

        # Check if there is something to switch one row below
        if (dr + 1) <= SIZE - 1:
            new_grid[dr + 1][dc] ^= 1

        # Check if there is something to switch to the left
        if (dc - 1) >= 0:
            new_grid[dr][dc - 1] ^= 1

        # Check if there is something to switch to the right
        if (dc + 1) <= SIZE - 1:
            new_grid[dr][dc + 1] ^= 1


    # Display the board every turn
    def display(self):
        for r in range(SIZE):
            for c in range(SIZE):
                # If it is a 0, print an "off" tile
                if self.grid[r][c] == 0:
                    print("□", end='')
                # If it is a 1, print an "on" tile
                elif self.grid[r][c] == 1:
                    print("▣", end='')
            # Added for line breaking
            print()
        # Added for line breaking
        print()
