from analisis.classes.classes import Line, Island
from analisis.loader.img_analizer import is_neighbours
from logger import lg

def islands_from_lines(graph:list[Line]) -> list[Island]:
  lg.debug('first stage of the island build')
  complete:list[Island] = _first_graph_config(graph)
  lg.debug(f'complete with [{len(complete)}] islands')

  lg.debug('second stage of the island build')
  complete = _second_graph_config(complete)
  lg.debug(f'complete with [{len(complete)}] islands')
  return complete

def _first_graph_config(graph:list[Line]) -> list[Island]:
  raw_islands:list[Island] = []

  while (len(graph) != 0):
    temp = [graph[0]]

    for k in graph[1:]:
      if is_neighbours(temp[-1], k):
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
  while len(islands) > 0:
    isl_rest = 0
    
    while isl_rest < len(islands)-1:
      found = False
      _islands = islands[isl_rest]
      
      if (islands[-1].minW > _islands.maxW or
          islands[-1].maxW < _islands.minW or
          islands[-1].minH > _islands.maxH or
          islands[-1].maxH < _islands.minH):
          isl_rest += 1
          continue

      for line in _islands:
        arr_lines2:list[Line] = []
        
        for line2_offset in (-1,1):
          arr_lines2 = islands[-1].get_lines_at_index(line.index + line2_offset)
        
        for line2 in arr_lines2:
          if not is_neighbours(line, line2):
              islands[-1] = islands[-1] + _islands

              islands.remove(_islands)
              isl_rest = 0
              found = True
              break
        
      if not found: 
        isl_rest += 1

    complete.append(islands.pop())
  return complete
