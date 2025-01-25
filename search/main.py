from .aima.search import astar_search, breadth_first_graph_search
from .problem import SmartVacuumProblem, State
from .heuristics import h, h1, h2
from queue import LifoQueue
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from collections import deque

def draw_state(grid, position, action):
  n = len(grid)
  cell_size = 100
  img_size = n * cell_size
  img = Image.new(mode='RGB', size=(img_size, img_size), color='white')
  draw = ImageDraw.Draw(img)

  font = ImageFont.truetype("arial.ttf", 65)

  for row in range(n):
    for col in range(n):
      top_left = (col * cell_size, row * cell_size)
      bottom_right = ((col + 1) * cell_size, (row + 1) * cell_size)
      fill = None
      if (row, col) == position:
        fill = 'green'
        if action == 'CLEAN':
          fill = 'yellow'
      draw.rectangle([top_left, bottom_right], outline="black", width=2, fill=fill)

      textbbox = draw.textbbox(xy=(0,0),text=grid[row][col], font=font)
      text_width = textbbox[2] - textbbox[0]
      text_height = textbbox[3] - textbbox[1]
      text_position = (col * cell_size + (cell_size - text_width) // 2, row * cell_size + (cell_size - text_height) // 2 - 10)
      draw.text(text_position, grid[row][col], fill="black", font=font)

  return img

def neighbours(node, grid):
  neighbours = []
  (i,j) = node
  n = len(grid)
  valid_neighbours = ['V', 'D', 'F', 'C']
  if j<n-1 and grid[i][j+1] in valid_neighbours:
    #right
    neighbours.append((i, j+1))
  if i>0 and grid[i-1][j] in valid_neighbours:
    #up
    neighbours.append((i-1,j))
  if j>0 and grid[i][j-1] in valid_neighbours:
    # left
    neighbours.append((i, j-1))
  if i<n-1 and grid[i+1][j] in valid_neighbours:
    # down
    neighbours.append((i+1,j))
  return neighbours

def grid_has_solution(grid, start):
  to_visit = []
  for i,row in enumerate(grid):
    for j,cell in enumerate(row):
      if cell in ['V', 'D', 'F', 'S']:
         to_visit.append((i,j))

  frontier = deque([start])
  explored = set()
   
  while frontier:
    node = frontier.popleft()
    explored.add(node)
    for n in neighbours(node, grid):
        if n not in explored and n not in frontier:
          frontier.append(n)
  
  for cell in to_visit:
    if cell not in explored:
      return False
  return True


def draw_path(result):
  queue = LifoQueue()
  node = result
  while node:
    queue.put(node)
    node = node.parent

  while not queue.empty():
    node = queue.get()
    position = (node.state.pos_x, node.state.pos_y)
    grid = node.state.grid
    img = draw_state(grid=grid, position=position, action=node.action)
    plt.axis('off')
    plt.imshow(img)
    plt.show()

def solve_astar(grid):
  """accetta in input un array bidimensionale che rappresenta la griglia iniziale"""
  start = None
  for i in range(len(grid)):
      for j in range(len(grid[i])):
          if grid[i][j] == 'S':
              start = (i, j)
              break
          
  if not grid_has_solution(grid, start):
    return False
  
  initial_state = State(grid, start)
  problem = SmartVacuumProblem(initial=initial_state)

  result = astar_search(problem=problem, h=h)
  draw_path(result)
  
  return result

def solve_bfs(grid):
  start = None
  for i in range(len(grid)):
      for j in range(len(grid[i])):
          if grid[i][j] == 'S':
              start = (i, j)
              break
  
  if not grid_has_solution(grid, start):
    return False
  
  initial_state = State(grid, start)
  problem = SmartVacuumProblem(initial=initial_state)

  result = breadth_first_graph_search(problem)
  draw_path(result)

  return result