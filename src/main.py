from distutils.archive_util import make_archive
from pprint import pprint as pp
from copy import deepcopy

from cv2 import invert
from logger import lg

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import islands_from_lines, _second_graph_config
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_JPG, \
                  PATH_TO_INPUT_, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_MASK_, PATH_TO_OUTPUT_, \
                  PATH_TO_OUTPUT_JPG
lg.info("Start")

file = "test5.png"
# file = "input.jpg"
img:ndarray     = cv2.imread(PATH_TO_INPUT_ + file, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + file)

lg.info(f"load image '{file}'")
lg.debug(f"resolution '{file}' is {img.shape}")
completeFull:list[list[list[Island]]] = []

step_x = img.shape[1] // 8
# step_y = 80
step_y = img.shape[0] // 8

def fragment_calculate(coord_x:int, coord_y:int,
  step_x:int, step_y:int, mask_inv:np.ndarray) -> list[Island]:
    lines_arr = get_lines(mask_inv [
      coord_x:coord_x + step_x,
      coord_y:coord_y + step_y], coord_x, coord_y)
    complete = islands_from_lines(lines_arr)

    return complete

mask_inv = get_mask_from_gray(img, upper_val=100)
mask = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR) 

mask_array:list[np.ndarray] = []
up_value_from = 130
up_value_to = 140
up_value_step = 10

for up_value in range(up_value_from, up_value_to, up_value_step):
  mask_array.append(get_mask_from_gray(img, upper_val=up_value).copy())

isl = img_clr.copy()
cv2.imshow('w', isl)
# cv2.waitKey(0)
for i, mask in enumerate(mask_array):
  isl = img_clr.copy()
  for y in range(img.shape[0] // step_y):
    completeFull.append([])
    for x in range(img.shape[1] // step_x):
      # lg.debug(f">> step {i} [{x}|{y}][{x*step_x}, {y*step_y}]")

      # lines_arr = get_lines(mask_inv)
      # complete = islands_from_lines(lines_arr)

      complete = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask)
      # isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
      isl = draw_islands(complete, isl)
      isl = cv2.rectangle(isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))

      completeFull[y].append(complete.copy())

      lg.debug(f">> coord:{(x,y)}, black:{up_value_from + i*up_value_step}, found [{len(complete)}]")
      cv2.imshow('w', isl)
      cv2.waitKey(10)
  
cv2.imwrite(PATH_TO_MASK_ + "_test.png", isl)

del isl
isl:np.ndarray = img_clr.copy()
islands:list[Island] = []

for col in completeFull:
  cur_row:list[Island] = []
  for row in col:
    cur_row.extend(row)
    cur_row = _second_graph_config(cur_row)
  islands.append(cur_row)

  isl = draw_islands(cur_row, isl)
  cv2.imshow('w', isl)
  cv2.waitKey(10)

del completeFull

del isl
isl:np.ndarray = img_clr.copy()
complete_isl:list[Island] = []
for i, row in enumerate(islands):
  complete_isl.extend(row)
  complete_isl = _second_graph_config(sorted(complete_isl, key=len), check_bounds_top=(i-1)*step_y)
  isl = draw_islands(complete_isl, isl)
  cv2.imshow('w', isl)
  cv2.waitKey(10)
# cv2.waitKey(0)
cv2.imwrite(PATH_TO_OUTPUT_ + "islands.png", isl)

exit()

lines_arr = get_lines(mask_inv[:250,:250])
lg.debug(f"find [{len(lines_arr)}] lines")

complete = islands_from_lines(lines_arr)
lg.info(f"find [{len(complete)}] islands")

cv2.imwrite(PATH_TO_ISLANDS_JPG, draw_islands(complete, img_clr.copy(), draw_over=True))

# t = get_low_up(get_lines(mask_inv), img)
test_img = np.ones((img.shape[0],img.shape[1], 3)) * 255
complete[0].smooth()
test_isl:Island = deepcopy(complete[0])
# test_isl.set_wide_x2()

# pnt = get_low_up(test_isl, test_img)
# # pnt = get_low_up(complete[0], test_img)
test_img = draw_islands(complete, test_img)
# sum_avg = 0
# step = 4

# for i in range(step):
#   sum_avg += pnt[i]

# test_img[step-1, int(sum_avg / step)] = (255,0,0)

# t = len(pnt)
# for i, j in enumerate(pnt[step:]):
#   sum_avg = sum_avg - pnt[i] + pnt[i+step]
#   test_img[int(sum_avg/step), complete[0][0].index + i + step] = (255,0,0)

cv2.imwrite(PATH_TO_MASK_JPG, img)
cv2.imwrite(PATH_TO_MASK_ + "_test.png", test_img)
lg.info("complete")

# cv2.imwrite(PATH_TO_OUTPUT_JPG,img)
# cv2.imwrite(r'../images/output/output.png',blank3)