from Project1.puzzles.lightsout import Lightsout
from Project1.agents.astar import AStarAgent

# Initialize the puzzle
puzzle = Lightsout()
# Initialize the agent
agent = AStarAgent()
# Have the agent solve the puzzle
agent.solve(puzzle)
