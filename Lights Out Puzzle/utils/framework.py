from time import sleep, time


# Superclass for puzzles
class Puzzle(object):

    # Return whether this puzzle is equivalent to the other
    def __eq__(self, other):
        raise NotImplementedError

    # Return a hash code for this puzzle
    def __hash__(self):
        raise NotImplementedError

    # Return whether this puzzle comes before the other in a sort
    def __lt__(self, other):
        raise NotImplementedError

    # Return whether this puzzle is solved
    def solved(self):
        raise NotImplementedError

    # Return an estimate of how far this puzzle is from being solved
    def heuristic(self):
        raise NotImplementedError

    # Return a list of legal moves
    def moves(self):
        raise NotImplementedError

    # Return a new puzzle created by a move
    def neighbor(self, move):
        raise NotImplementedError

    # Print this puzzle to the console
    def display(self):
        raise NotImplementedError

    # Conduct this game
    def play(self, player, interval=1):
        # Let the user know they are playing
        print("Playing game:")
        # Display the board
        self.display()
        # Keep track of moves
        moves = 0

        # Set the game
        game = self

        # While the game is not over
        while game.heuristic() != 0:
            # Start a timer to let user know time it takes
            start = time()
            # Get the move of the player
            move = player.move(game)
            # See how long it took
            seconds = time() - start

            # Tell user how long it took them
            print("It took ", seconds, "seconds to make your move.")

            # Save the new game
            game = game.neighbor(move)
            # Display the new game
            game.display()
            # Increment move counter
            moves += 1

            # Sleep the game to give user a second
            sleep(interval)

        # If we reach here, game is over.
        print("You win" + "after", moves, "moves!!")


# Superclass for a puzzle solver
class Agent(object):

    # Return the move this agent wants to make
    def move(self, puzzle):
        raise NotImplementedError

    # Watch this agent solve a puzzle
    def solve(self, puzzle, interval=0.25):
        # Tell user puzzle is being solved
        print("solving puzzle:")
        # Display the puzzle
        puzzle.display()
        # Save the moves
        moves = 0

        # While the puzzle is still not solved
        while not puzzle.solved():

            # Start a time
            start = time()
            # Save the move
            move = self.move(puzzle)
            # Stop the timer
            seconds = time() - start

            # Print time it took for the move
            print("After", seconds, "seconds:")
            # Save the new puzzle
            puzzle = puzzle.neighbor(move)
            # Display the new puzzle
            puzzle.display()
            # Increment counter
            moves += 1

            # Sleep algorithm for a second for cleaner output
            sleep(interval)

        # If we reach here, puzzle is solved.
        print("Puzzle solved in", moves, "moves.")
