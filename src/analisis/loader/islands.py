from cmath import inf, nan
from copyreg import pickle
from analisis.classes.classes import Line, Island
from analisis.loader.img_analizer import is_not_neighbours
from logger import lg
import pickle
import numpy as np
import cv2

def islands_from_lines(graph:list[Line]) -> list[Island]:
  complete:list[Island] 
  
  complete = _first_graph_config(graph)
  complete = _second_graph_config(sorted(complete, key=len))
  return complete

def _first_graph_config(graph:list[Line]) -> list[Island]:
  raw_islands:list[Island] = []
  graph = sorted(graph)
  
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
  write_counter = 0
  while len(islands) > 0:
    isl_rest = 0
    
    while isl_rest < len(islands)-1:
      found = False
      cur_island = islands[isl_rest]
      last_island = islands[-1]
      
      if (last_island.minW -1 > cur_island.maxW or
          last_island.maxW +1 < cur_island.minW or
          last_island.minH -1 > cur_island.maxH or
          last_island.maxH +1 < cur_island.minH):
          isl_rest += 1
          continue
      
      for line in cur_island:
        arr_lines2:list[Line] = []

        for line2_offset in (-1,0,1):
          arr_lines2.extend(last_island.get_lines_at_index(line.index + line2_offset, check_bounds_top, line.down))
        if len(arr_lines2) == 0: continue

        neighbours_arr = map(lambda l: not is_not_neighbours(line, l), arr_lines2)
        condition = any([i for i in neighbours_arr])
        ll2 = [not is_not_neighbours(l, line) for l in arr_lines2]
        if condition:
          dt1 = {}
          dt2 = {}
          # with open('test1.bin', 'rb') as f: 
          #   dt1 = pickle.load(f)
          # with open('test2.bin', 'rb') as f: 
          #   dt2 = pickle.load(f)
          
          # if (write_counter == 0 and len(dt1.keys()) != 0): 
          #   write_counter = max(dt1.keys())

          # dt1[write_counter] = line
          # dt2[write_counter] = arr_lines2
          
          # with open("test1.bin", mode="wb") as f: 
          #   pickle.dump(dt1, f, protocol=pickle.HIGHEST_PROTOCOL)
          # with open("test2.bin", mode="wb") as f: 
          #   pickle.dump(dt2, f, protocol=pickle.HIGHEST_PROTOCOL)
          # write_counter += 1
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
