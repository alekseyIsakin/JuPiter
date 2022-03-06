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
      lines_to_check = [graph.pop(0)]

    while (len(lines_to_check) > 0):
      cur_line = lines_to_check.pop()
    
      arr_lines2 = []
      for line2_offset in (-1,0,1):
        arr_lines2.extend([l for l in graph if l.index == cur_line.index + line2_offset])
      
      for check_line in arr_lines2:
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

# def _first_graph_config_(graph:list[Line]) -> list[Island]:
#   raw_islands:list[Island] = []
#   graph = sorted(graph)
  
#   temp = [graph.pop(0)]
  
#   while (len(graph) != 0):
#     last_line = temp[-1]
    
#     arr_lines2 = []
#     for line2_offset in (-1,0,1):
#       arr_lines2.extend([l for l in graph if l.index == last_line.index + line2_offset])
    
#     have_no_neighbours = True
#     for check_line in arr_lines2:
#       if is_neighbours(last_line, check_line):
#         continue
#       have_no_neighbours = False
      
#       temp.append(check_line)
#       graph.remove(check_line)

#     if not have_no_neighbours: continue
#     isl = Island()

#     l = np.empty(len(temp), dtype=line_np_type)
#     l['index']  = np.array([l.index for l in temp ])
#     l['top']    = np.array([l.top   for l in temp ])
#     l['down']   = np.array([l.down  for l in temp ])

#     isl += l
#     # for i in temp:
#     #   graph.remove(i)
#     raw_islands.append(isl)
#   return raw_islands

def _second_graph_config(islands:list[Island], check_bounds_top=-inf, check_bounds_down=inf) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
          
  isl_rest = 0

  if (check_bounds_top != nan):
    while isl_rest < len(islands):
      if islands[isl_rest].down +1 < check_bounds_top:
        complete.append(islands.pop(isl_rest))
      else:
        isl_rest += 1
  # print('>'*10)
  # pp (islands)

  # if check_bounds_top != -inf:
  #   isl1 = draw_islands(complete, np.ones((670, 1280,3))*0)
  #   isl2 = draw_islands(islands, np.ones((670, 1280,3))*0)
  #   cv2.imshow('cut off', isl1)
  #   cv2.imshow('remais', isl2)
    # cv2.waitKey(200)
  arr_lines2:list[Line] = []
  arr_clear = arr_lines2.clear
  arr_extend = arr_lines2.extend
  
  while len(islands) > 0:
    isl_rest = 0
    while isl_rest < len(islands)-1:
      found = False
      cur_island = islands[isl_rest]
      last_island = islands[-1]
      get_nearest_lines = last_island.get_lines_at_index
      # pp(cur_island)
      # pp(last_island)

      if (last_island.right +1 < cur_island.left  or
          last_island.left  -1 > cur_island.right or
          last_island.down  +1 < cur_island.top   or
          last_island.top   -1 > cur_island.down):
          isl_rest += 1
          continue

      for line in cur_island:
        arr_clear()

        for line2_offset in (-1,0,1):
          arr_extend(get_nearest_lines(line['index'] + line2_offset, check_bounds_top, line['down']))
        if len(arr_lines2) == 0: continue

        neighbours_arr = map(lambda l: is_neighbours(line, l), arr_lines2)
        condition = any([i for i in neighbours_arr])

        if not condition:
          continue

        last_island = last_island + cur_island

        del islands[isl_rest]
        # islands.remove(cur_island)
        isl_rest = 0
        found = True
        break
        
      if not found: 
        isl_rest += 1

    complete.append(islands.pop())
  return complete
