from solving.puzzles.maze import Maze
from solving.agents.astar import AStarAgent

puzzle = Maze()
agent = AStarAgent()
agent.solve(puzzle)