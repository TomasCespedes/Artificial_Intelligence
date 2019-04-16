from Project1.puzzles.lightsout import Lightsout
from Project1.agents.iterativedeepening_astar import IterativeAStarAgent

# Initialize the puzzle
puzzle = Lightsout()
# Initialize the agent
agent = IterativeAStarAgent()
# Have the agent solve the puzzle
agent.solve(puzzle)
