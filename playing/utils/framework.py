from time import time, sleep


# Superclass for all games
class Game(object):

    # Return whether this game is equivalent to the other
    def __eq__(self, other):
        raise NotImplementedError

    # Return a hash code for this game
    def __hash__(self):
        raise NotImplementedError

    # Return the utility of this game (if it's over)
    # If this game isn't over yet, return None
    def utility(self):
        raise NotImplementedError

    # Return a list of legal moves
    def moves(self):
        raise NotImplementedError

    # Return a new game created by a move
    def child(self, move, player):
        raise NotImplementedError

    # Print this game to the console
    def display(self):
        raise NotImplementedError

    # Conduct this game
    def play(self, max_player, min_player, interval=1):
        print("Playing game:")
        self.display()
        moves = 0

        game = self
        player, opponent = max_player, min_player

        while game.utility() is None:

            start = time()
            move = player.move(game)
            seconds = time() - start

            if player.maximizes():
                print("MAX after", seconds, "seconds:")
            else:
                print("MIN after", seconds, "seconds:")

            game = game.child(move, player)
            game.display()
            moves += 1

            sleep(interval)
            player, opponent = opponent, player

        print("Game over with utility", game.utility(), "after", moves, "moves")


# Superclass for all players
class Player(object):

    # Return whether this player wants to maximize utility
    def maximizes(self):
        raise NotImplementedError

    # Return the move this player wants to make
    def move(self, game):
        raise NotImplementedError
