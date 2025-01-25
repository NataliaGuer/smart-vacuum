def get_cells_traversed_by_line(line_start: tuple[int, int], line_end: tuple[int, int]) -> list[tuple[int, int]]:
  """Get the cells traversed by a line from start to end using Bresenham's Line Algorithm."""
  cells = []
  x0, y0 = line_start
  x1, y1 = line_end
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  x = x0
  y = y0
  n = 1 + dx + dy
  x_inc = 1 if x1 > x0 else -1
  y_inc = 1 if y1 > y0 else -1
  error = dx - dy
  dx *= 2
  dy *= 2

  for _ in range(n):
    cells.append((x, y))
    if error > 0:
      x += x_inc
      error -= dy
    else:
      y += y_inc
      error += dx
  
  cells.remove(line_start)
  cells.remove(line_end)

  return cells