from playing.utils.framework import Game


class Stones(Game):

    def __init__(self, stones, last_player=None):
        self.stones = stones
        self.last_player = last_player

    def __eq__(self, other):
        return self.stones == other.stones

    def __hash__(self):
        return hash(self.stones)

    def utility(self):
        if self.stones == 0:
            if self.last_player.maximizes():
                return -1
            else:
                return +1

    def moves(self):
        moves = [1]
        if self.stones >= 2:
            moves.append(2)
        if self.stones >= 3:
            moves.append(3)
        return moves

    def child(self, move, player):
        return Stones(self.stones - move, player)

    def display(self):
        print(self.stones, end='\n\n')
