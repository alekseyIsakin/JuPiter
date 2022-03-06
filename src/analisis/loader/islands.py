from cmath import inf, nan
import cv2

import numpy as np
from analisis.classes.classes import Line, Island
from analisis.loader.img_analizer import is_not_neighbours
from drawing.draw import draw_islands
from logger import lg

def islands_from_lines(graph:list[Line]) -> list[Island]:
  complete:list[Island] 
  
  complete = _first_graph_config(graph)
  complete = _second_graph_config(sorted(complete, key=len))
  return complete

def _first_graph_config(graph:list[Line]) -> list[Island]:
  raw_islands:list[Island] = []

  while (len(graph) != 0):
    temp = [graph[0]]

    for k in graph[1:]:
      if is_not_neighbours(temp[-1], k):
        # slow_draw_islands([[temp[-1]], [k]], img_clr.copy(), clr=(0,0,255), sleeptime=100, draw_over=True, scale=(3,3))
        continue
      
      temp.append(k)
    
    # slow_draw_island(temp, img_clr.copy(), sleeptime=500, clr=(0,255,0), draw_over=True)
    isl = Island()

    for i in temp:
      isl.append_one_line(i)
      graph.remove(i)
    raw_islands.append(isl)
  return raw_islands


def _second_graph_config(islands:list[Island], check_bounds_top=-inf, check_bounds_down=inf) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
          
  isl_rest = 0
  if (check_bounds_top != nan):
    while isl_rest < len(islands):
      if islands[isl_rest].maxH < check_bounds_top:
        complete.append(islands.pop(isl_rest))
      else:
        isl_rest += 1
  # if check_bounds_top != -inf:
  #   isl1 = draw_islands(complete, np.ones((670, 1280))*0)
  #   isl2 = draw_islands(islands, np.ones((670, 1280))*0)
  #   cv2.imshow('q', isl1)
  #   cv2.imshow('z', isl2)
  #   cv2.waitKey(200)

  arr_lines2:list[Line] = []
  arr_extend = arr_lines2.extend
  arr_clear = arr_lines2.clear
  while len(islands) > 0:
    isl_rest = 0
    
    while isl_rest < len(islands)-1:
      found = False
      cur_island = islands[isl_rest]
      last_island = islands[-1]
      get_nearest_lines = last_island.get_lines_at_index
      
      if (last_island.minW -1 > cur_island.maxW or
          last_island.maxW +1 < cur_island.minW or
          last_island.minH -1 > cur_island.maxH or
          last_island.maxH +1 < cur_island.minH):
          isl_rest += 1
          continue

      for line in cur_island:
        arr_clear()

        for line2_offset in (-1,0,1):
          arr_extend(get_nearest_lines (line.index + line2_offset, check_bounds_top, line.down))
        if len(arr_lines2) == 0: continue

        for line2 in arr_lines2:
          if is_not_neighbours(line, line2): continue
          last_island = last_island + cur_island

          del islands[isl_rest]
          # islands.remove(cur_island)
          isl_rest = 0
          found = True
          break
        if found: break
        
      if not found: 
        isl_rest += 1

    complete.append(islands.pop())
  return complete
