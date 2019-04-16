from Project1.puzzles.lightsout import Lightsout
from Project1.agents.iterativedeepening import IterativeDeepeningAgent

# Initialize the puzzle
puzzle = Lightsout()
# Initialize the agent
agent = IterativeDeepeningAgent()
# Have the agent solve the puzzle
agent.solve(puzzle)
