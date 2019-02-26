from solving.puzzles.queens import Queens
from solving.agents.climb import HillClimbingAgent


puzzle = Queens()
agent = HillClimbingAgent()
agent.solve(puzzle)

