from asyncio.windows_events import NULL
from cmath import inf, nan
import numpy as np
import cv2

line_np_type = np.dtype([('index', np.int32),('top', np.int32),('down', np.int32)])

class Line():
  def __init__(self, index, top, down) -> None:
    self.index = index
    self.down = down
    self.top = top

  def __getitem__(self, key):
    if key == 0 or key == 'index': return self.index
    if key == 1 or key == 'top':   return self.top
    if key == 2 or key == 'down':  return self.down
    
  def __repr__(self):
    return ("{ index: " + str(self.index) + ", " +\
            "top: " + str(self.top) + ", "+ \
            "down: " + str(self.down) + "}")
  
  def __lt__(self, other):
    return self.index < other.index
  def __le__(self, other):
    return self.index <= other.index
  def __gt__(self, other):
    return self.index > other.index
  def __ge__(self, other):
    return self.index >= other.index
  def __eq__(self, other):
    return (self.index == other.index and
            self.top == other.top and
            self.down == other.down)      

  def is_neighbour(self, other)->bool:
    if (abs(self.index - other.index) > 1): return False
    if ((self.top <= (other.top+1) and self.top >= (other.down-1)) or
          (self.down <= (other.top+1) and self.down >= (other.down-1)) or
          (other.top <= (self.top+1) and other.top >= (self.down-1))  or
          (other.down <= (self.top+1) and other.down >= (self.down-1))): return True
    return False

class Island():
  def __init__(self):
    self.top = 0
    self.left = 0
    self.down = 0
    self.right = 0
    self.lines = np.empty(0, dtype=line_np_type)
    pass

  def __getitem__(self, key) -> Line:
    return self.lines[key]
  
  def __len__(self) -> int:
    return len(self.lines)
  
  def get_lines_at_index(self, index:int, top:int=-inf, down:int=inf) -> list[Line]:
    if (index >= self.right or index <= self.left):
      return []
    # if (top > self.minH +1 and down < self.maxH -1):
    #   return []
    return [l for l in self.lines if (l['index'] == index) and (l['down'] > top-1)]

  def sort(self) -> None:
    self.lines = np.sort(self.lines)

  def smooth(self):
    # newlines = [self.lines[0]]
    newlines = np.empty(0, dtype=line_np_type)

    newlines = np.append(newlines, self.lines[0])

    for l in self.lines[1:]:
      if newlines[-1].index != l.index:
        newlines = np.append(newlines, l)
        continue
      newlines[-1].top  = max(newlines[-1].top,  l.top)
      newlines[-1].down = min(newlines[-1].down, l.down)
    self.lines = newlines

  def __add__(self, other):
    tmp = np.empty(len(self.lines) + len(other), dtype=line_np_type)

    v =  np.concatenate((self.lines, other))
    tmp = v
    self.top = int(np.min(tmp['top']))       # topY
    self.left = int(np.min(tmp['index']))     # topX
    self.down = int(np.max(tmp['down']))      # downY
    self.right = int(np.max(tmp['index']))     # downX

    self.lines = np.sort(tmp)
    return self

  def __repr__(self):
    return f"<Island. Top: [{self.left}, {self.top}], Bottom: [{self.right}, {self.down}]>"