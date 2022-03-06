from cmath import inf
import cv2
import numpy as np
import random as rnd

from analisis.classes.classes import Line, Island

def get_lines(mask_inv:np.ndarray, offset_x=0, offset_y=0) -> list[Line]:
    graph = []

    for j in range(mask_inv.shape[1]):
        higher = inf
        lower = -inf

        cntBlank = 0
        lines = []

        for i in range(mask_inv.shape[0]):
            if mask_inv[i,j] == 255: 
                cntBlank += 1
                if lower == -inf:
                    continue
            
            if lower == -inf: lower = i
            if mask_inv[i,j] != 255: 
                higher = i
                cntBlank = 0
            if cntBlank > 0:
                lines.append(Line(j+offset_y, lower+offset_x, higher+offset_x))
                lower = -inf
                higher = inf
        if lower > 0:
            lines.append(Line(j+offset_y, lower+offset_x, higher+offset_x))
        for l in lines:
            graph.append(l)
        lines.clear()
    
    return graph



def get_low_up(graph:list[Island], img=np.zeros(0)) -> list[int]:

    prev = graph[0]

    prevPoint = 0
    mainPoints = []
    mainPoints.append(graph[0].top)
    prevPoint = graph[0].down
    status = False
    shape = len(img.shape)
    print("Я начну с точки ", mainPoints[0])

    if shape > 1:
        if shape == 2:
            clr = 25
        else:
            clr = (0, 255, 0)
        img[mainPoints[0]][graph[0].index] = clr

    for p in graph[1:]:
            
        if(status == False):
            if(mainPoints[-1] < p.top):
                if(prevPoint <= p.down):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    if((p.top - mainPoints[-1]) > (p.down - prevPoint)):
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
                    elif((p.top - mainPoints[-1]) < (p.down - prevPoint)):
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
                    else:
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
            elif(mainPoints[-1] > p.top):
                if(prevPoint >= p.down):
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
                else:
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
            else:
                if(prevPoint <= p.down):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
        else:
            if(mainPoints[-1] > p.down):
                if(prevPoint >= p.top):
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
                else:
                    if((p.down - mainPoints[-1]) < (p.top - prevPoint)):
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
                    elif((p.down - mainPoints[-1]) > (p.top - prevPoint)):
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
                    else:
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
            elif(mainPoints[-1] < p.down):
                status = False
                mainPoints.append(p.top)
                prevPoint = p.down
            else:
                if(p.top > prevPoint):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
                    
        if shape > 1:
            if shape == 2:
                clr = 200
            else:
                clr = (0, 255, 0)
            
            cv2.line(img, (p[0],p[2]), (p[0], p[1]), clr)
            
            if len(img.shape) == 2:
                clr = 255 if status else 0
            else:
                clr = (255, 255, 0) \
                    if status else (0, 255, 255)
            clr = (0,0,255)
            img[mainPoints[-1]][p.index] = clr

    # if len(img.shape) > 1:
    #     cv2.imwrite(PATH_TO_OUTPUT_JPG,img)

    return mainPoints
  
def is_not_neighbours(left_line=Line(0,0,0), right_line=Line(0,0,0)):
    if left_line == right_line: return False
    
    t1 = not abs(left_line['index'] - right_line['index']) > 1
    t2 = (left_line['down'] <= right_line['down']+1 and left_line['down'] >= (right_line['top']-1))
    t3 = (left_line['top'] <= (right_line['down']+1) and left_line['top'] >= (right_line['top']-1))
    t4 = (right_line['down'] <= (left_line['down']+1) and right_line['down'] >= (left_line['top']-1))
    t5 = (right_line['top'] <= (left_line['down']+1) and right_line['top'] >= (left_line['top']-1))
    t6 = not (t1 and (t2 or t3 or t4 or t5))
    return t6
  
def is_not_neighbours_(l=Line(0,0,0), r=Line(0,0,0)):
    if l == r: return False
    return not (not abs(l.index - r.index) > 1 and 
         ((l.top <= (r.top+1) and l.top >= (r.down-1)) or
          (l.down <= (r.top+1) and l.down >= (r.down-1)) or
          (r.top <= (l.top+1) and r.top >= (l.down-1))  or
          (r.down <= (l.top+1) and r.down >= (l.down-1))))