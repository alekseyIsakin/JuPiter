from analisis.classes.classes import Line, Island
from analisis.loader.img_analizer import is_not_neighbours
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


def _second_graph_config(islands:list[Island]) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
  
  # while isl_rest < len(islands)-1:
  #   small_isl = islands[isl_rest]
  #   in_bound = False
  #   for cur_isl in islands:
  #     if not (cur_isl.minW > small_isl.maxW  or
  #             cur_isl.maxW < small_isl.minW  or
  #             cur_isl.minH > small_isl.maxH  or
  #             cur_isl.maxH < small_isl.minH ): 
  #         isl_rest += 1
  #         in_bound = True
  #         break
    
  #   if not in_bound:
  #     complete.append(islands.pop(isl_rest))
          
  print(f"{len(complete)}")
  isl_rest = 0
  while len(islands) > 0:
    isl_rest = 0
    
    while isl_rest < len(islands)-1:
      found = False
      cur_island = islands[isl_rest]
      last_island = islands[-1]
      
      if (last_island.minW > cur_island.maxW or
          last_island.maxW < cur_island.minW or
          last_island.minH > cur_island.maxH or
          last_island.maxH < cur_island.minH):
          isl_rest += 1
          continue
      
      for line in cur_island:
        arr_lines2:list[Line] = []
        
        for line2_offset in (-1,1):
          arr_lines2.extend(last_island.get_lines_at_index(line.index + line2_offset))
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
        
      lg.info(f'{isl_rest}')
      if not found: 
        isl_rest += 1

    complete.append(islands.pop())
  return complete
