from .aima.search import Problem
import copy

class State:

  def __init__(self, grid: list[list[int]], position: tuple[int, int]):
    self.grid = grid
    self.pos_x = position[0]
    self.pos_y = position[1]
  
  def getRoomState(self):
    return self.grid[self.pos_x][self.pos_y]

class SmartVacuumProblem(Problem):

  def __init__(self, initial: State, goal=None):
    super().__init__(initial, goal)

  def actions(self, state: State) -> list[str]:
    room_state = state.getRoomState()
    grid = state.grid
    n = len(grid)-1
    actions = ['CLEAN','UP', 'DOWN', 'LEFT', 'RIGHT']
    if state.pos_x == 0 or grid[state.pos_x-1][state.pos_y] == 'X':
      actions.remove('UP')
    if state.pos_x == n or grid[state.pos_x+1][state.pos_y] == 'X':
      actions.remove('DOWN')
    if state.pos_y == 0 or grid[state.pos_x][state.pos_y-1] == 'X':
      actions.remove('LEFT')
    if state.pos_y == n or grid[state.pos_x][state.pos_y+1] == 'X':
      actions.remove('RIGHT')
    if room_state in ['C', 'S', 'F']:
      actions.remove('CLEAN')
    return actions

  def result(self, state, action):
      # action can be UP, DOWN, LEFT, RIGHT, CLEAN
      # CLEAN applied to a Dirty room results in a Clean room
      # CLEAN applied to a Very dirty room results in a Dirty room
      result_state = copy.deepcopy(state)
      if (action == 'UP'):
        result_state.pos_x -= 1
      elif (action == 'DOWN'):
        result_state.pos_x += 1
      elif (action == 'LEFT'):
        result_state.pos_y -= 1
      elif (action == 'RIGHT'):
        result_state.pos_y += 1
      elif (action == 'CLEAN'):
        if (state.getRoomState() == 'D'):
          result_state.grid[state.pos_x][state.pos_y] = 'C'
        elif(state.getRoomState() == 'V'):
          result_state.grid[state.pos_x][state.pos_y] = 'D'

      return result_state

  def goal_test(self, state):
    return all(room in ['C', 'S', 'F', 'X'] for row in state.grid for room in row) and state.getRoomState() == 'F'