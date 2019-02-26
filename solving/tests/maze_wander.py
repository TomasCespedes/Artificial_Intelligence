from solving.puzzles.maze import Maze
from solving.agents.wander import WanderAgent

puzzle = Maze()
agent = WanderAgent()
agent.solve(puzzle)