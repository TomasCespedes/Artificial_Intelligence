from Project1.puzzles.lightsout import Lightsout
from Project1.agents.bfs import BFSAgent

puzzle = Lightsout()
agent = BFSAgent()
agent.solve(puzzle)