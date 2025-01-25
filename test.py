from search.main import solve_bfs, grid_has_solution, solve_astar
from search.heuristics import h, h1
from search.aima.search import Node
from search.problem import State

grid = [['V', 'X', 'D', 'C', 'C', 'D'],
 ['V', 'D', 'X', 'D', 'V', 'C'],
 ['C', 'D', 'C', 'V', 'V', 'V'],
 ['X', 'V', 'V', 'V', 'V', 'D'],
 ['C', 'C', 'S', 'D', 'D', 'V'],
 ['V', 'V', 'X', 'F', 'C', 'C']]

state = State(grid, (4,2))
node = Node(state)

print(h1(node))
res = solve_astar(grid)
