from LightsOutPuzzle.puzzles.lightsout import Lightsout
from LightsOutPuzzle.agents.bfs import BFSAgent

puzzle = Lightsout()
agent = BFSAgent()
agent.solve(puzzle)