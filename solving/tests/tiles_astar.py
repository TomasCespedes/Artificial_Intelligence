from solving.puzzles.tiles import Tiles
from solving.agents.astar import AStarAgent

puzzle = Tiles()
agent = AStarAgent()
agent.solve(puzzle)