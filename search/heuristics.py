from heapq import heappop, heappush
from .aima.search import Node

def mst_cost(grid: list[list[str]]) -> int:
  nodes = []

  for i,row in enumerate(grid):
    for j,cell in enumerate(row):
      if cell in ['S', 'D', 'V', 'F']:
        nodes.append((cell, i, j))

  graph = {cell: [] for cell in nodes}
  for i, cell1 in enumerate(nodes):
    for j, cell2 in enumerate(nodes):
      if i != j:
        distance = abs(cell1[1] - cell2[1]) + abs(cell1[2] - cell2[2])
        graph[cell1].append((distance, cell2))

  start = nodes[0]
  visited = set()
  mst_cost = 0
  heap = [(0, start)]

  while heap:
    cost, node = heappop(heap)
    if node not in visited:
      visited.add(node)
      mst_cost += cost
      for edge_cost, neighbour in graph[node]:
        if neighbour not in visited:
          heappush(heap, (edge_cost, neighbour))

  return mst_cost

def cleaning_cost(grid: list[list[str]]) -> int:
  cleaning = 0
  for row in grid:
    for room in row:
      if room == 'D':
        cleaning += 1
      elif room == 'V':
        cleaning += 2
  return cleaning

def distance_to_goal(node: Node) -> int:
  grid = node.state.grid
  for i,row in enumerate(grid):
    for j,cell in enumerate(row):
      if cell == 'F':
        return abs(node.state.pos_x - i) + abs(node.state.pos_y - j)

def distance_to_closest_dirty_cell(grid: list[list[str]], cell: tuple[int, int]) -> int:
  
  if grid[cell[0]][cell[1]] in ['D', 'V']:
    return 0

  min_distance = float('inf')

  for i,row in enumerate(grid):
    for j,current_cell in enumerate(row):
      if current_cell in ['D', 'V']:
        if (i,j) != cell:
          distance = abs(cell[0] - i) + abs(cell[1] - j)
          if distance < min_distance:
            min_distance = distance
  
  return min_distance

def adiacent_cells_cost(grid, position):
  cost = 0
  n = len(grid)
  i_start = max(position[0]-1, 0)
  i_end = min(position[0]+1, n-1)
  j_start = max(position[1]-1, 0)
  j_end = min(position[1]+1, n-1)
  for i in range(i_start, i_end+1):
    for j in range(j_start, j_end+1):
      if grid[i][j] == 'D':
        cost += 1
      if grid[i][j] == 'V':
        cost += 2
      if grid[i][j] in ['D', 'V']:
        cost += abs(position[0] - i) + abs(position[1] - j)
  return cost

def h(node: Node) -> float:
  if all(el in ['C', 'S', 'F', 'X'] for row in node.state.grid for el in row):
    return distance_to_goal(node)
  return distance_to_closest_dirty_cell(grid=node.state.grid, cell=(node.state.pos_x, node.state.pos_y)) + cleaning_cost(node.state.grid)*3 + mst_cost(node.state.grid)

def h1(node: Node) -> int:
  if all(el in ['C', 'S', 'F', 'X'] for row in node.state.grid for el in row):
    return distance_to_goal(node)
  return adiacent_cells_cost(node.state.grid, (node.state.pos_x, node.state.pos_y))

def h2(node: Node) -> float:
  if all(el in ['C', 'S', 'F', 'X'] for row in node.state.grid for el in row):
    return distance_to_goal(node)/2
  return cleaning_cost(node.state.grid) + mst_cost(node.state.grid)