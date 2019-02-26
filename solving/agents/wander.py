from solving.utils.framework import Agent
from random import choice


class WanderAgent(Agent):

    def move(self, puzzle):
        return choice(puzzle.moves())



