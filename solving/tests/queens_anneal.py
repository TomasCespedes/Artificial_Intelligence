from solving.puzzles.queens import Queens
from solving.agents.anneal import SimulatedAnnealingAgent

puzzle = Queens()
agent = SimulatedAnnealingAgent()
agent.solve(puzzle)