from solving.puzzles.tiles import Tiles
from solving.agents.bfs import BFSAgent


puzzle = Tiles()
agent = BFSAgent()
agent.solve(puzzle)