from Project1.puzzles.lightsout import Lightsout
from Project1.agents.astar import AStarAgent

puzzle = Lightsout()
agent = AStarAgent()
agent.solve(puzzle)