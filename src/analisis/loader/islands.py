from cmath import inf, nan
from copyreg import pickle
from time import time
from analisis.classes.classes import Line, Island, line_np_type
from analisis.loader.img_analizer import is_neighbours
from drawing.draw import draw_islands
from logger import lg
from pprint import pp
import pickle
import numpy as np
import cv2

def islands_from_lines(graph:list[Line]) -> list[Island]:
  complete:list[Island] 
  
  complete = _first_graph_config(graph)
  # complete = _second_graph_config(sorted(complete, key=len))
  return complete

def _first_graph_config(graph:list[Line]) -> list[Island]:
  if (len(graph) == 0):
    return []

  raw_islands:list[Island] = []
  graph = sorted(graph)
  lines_complete:list[Line]  = []
  lines_to_check:list[Line] = [graph.pop(0)]
  
  new_check_line = lines_to_check.append
  new_complete_line = lines_complete.append
  remove_line = graph.remove

  while (len(graph) != 0 or len(lines_to_check) != 0):
    lines_complete.clear()
    if (len(lines_to_check) == 0 and len(graph) != 0):
      lines_to_check.append(graph.pop(0))

    while (len(lines_to_check) > 0):
      cur_line = lines_to_check.pop()
    
      arr_lines = []
      for line2_offset in (-1,0,1):
        arr_lines.extend([l for l in graph if l.index == cur_line.index + line2_offset])
      
      for check_line in arr_lines:
        if not is_neighbours(cur_line, check_line):
          continue
        
        lines_to_check.append(check_line)
        remove_line(check_line)
      new_complete_line(cur_line)
    

    isl = Island()

    l = np.empty(len(lines_complete), dtype=line_np_type)
    l['index']  = np.array([l.index for l in lines_complete ])
    l['top']    = np.array([l.top   for l in lines_complete ])
    l['down']   = np.array([l.down  for l in lines_complete ])

    isl += l
    # for i in temp:
    #   graph.remove(i)
    raw_islands.append(isl)
  return raw_islands

def _second_graph_config(islands:list[Island], top_bound=-inf, left_bound=-inf) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
          
  isl_rest = 0

  while isl_rest < len(islands):
    if (islands[isl_rest].down  +1 < top_bound or 
        islands[isl_rest].right +1 < left_bound) :
      complete.append(islands.pop(isl_rest))
    else:
      isl_rest += 1
  
  if (len(islands) == 0):
    return complete

  remove_isl_gen = islands.remove

  islands_to_check:list[Island] = [islands.pop()]
  add_check_isl = islands_to_check.append
  pop_check_isl = islands_to_check.pop

  future_island:list[Island]    = []
  add_future_isl = future_island.append

  arr_lines:list[Line] = []
  arr_extend = arr_lines.extend
  arr_clear = arr_lines.clear

  check_lines = []
  check_l_clear = check_lines.clear
  check_extend = check_lines.extend

  while len(islands) > 0 or len(islands_to_check) > 0:
    future_island.clear()

    if (len(islands_to_check) == 0 and len(islands) != 0):
      add_check_isl(islands.pop())

    while (len(islands_to_check) > 0):
      cur_isl = pop_check_isl()

      for check_isl in islands:
        if (cur_isl.right +1 < check_isl.left  or
            cur_isl.left  -1 > check_isl.right or
            cur_isl.down  +1 < check_isl.top   or
            cur_isl.top   -1 > check_isl.down):
            continue
        check_isl_lines = check_isl.get_lines_at_index
        cur_isl_lines = cur_isl.get_lines_at_index
        check_l_clear()

        if left_bound == -inf:
          check_lines = cur_isl.lines 
        else:
          check_extend(cur_isl_lines(left_bound - 1))
          check_extend(cur_isl_lines(left_bound + 0))
          check_extend(cur_isl_lines(left_bound + 1))

        for line in check_lines:
          arr_clear()

          for line2_offset in (-1,0,1):
            arr_extend(check_isl_lines(line['index'] + line2_offset, top_bound, line['down']))
          if len(arr_lines) == 0: continue

          found = False
          for line2 in arr_lines:
            if not is_neighbours(line, line2): continue

            # islands.remove(cur_island)
            found = True
            add_check_isl(check_isl)
            break
          if found: break
      
      for i in [isl for isl in islands_to_check if isl in islands]:
        remove_isl_gen(i)

      add_future_isl(cur_isl)
    isl = Island()
    for i in future_island:
    # for i in sorted(future_island, key=len):
      isl += i
    complete.append(isl)
  return complete
