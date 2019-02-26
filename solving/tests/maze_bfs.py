from solving.puzzles.maze import Maze
from solving.agents.bfs import BFSAgent

puzzle = Maze()
agent = BFSAgent()
agent.solve(puzzle)