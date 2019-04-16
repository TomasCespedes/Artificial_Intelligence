from LightsOutPuzzle.puzzles.lightsout import Lightsout
from LightsOutPuzzle.agents.iterativedeepening import IterativeDeepeningAgent

# Initialize the puzzle
puzzle = Lightsout()
# Initialize the agent
agent = IterativeDeepeningAgent()
# Have the agent solve the puzzle
agent.solve(puzzle)
