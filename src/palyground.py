from pprint import pprint as pp
from copy import deepcopy

from cv2 import imwrite

from logger import lg

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import islands_from_lines
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_IMAGES, PATH_TO_INPUT_JPG, \
                  PATH_TO_INPUT_, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_MASK_, \
                  PATH_TO_OUTPUT_

import pickle

lg.info("palyground start")
file = "input.jpg"
img:ndarray     = cv2.imread(PATH_TO_INPUT_ + file, cv2.IMREAD_GRAYSCALE)
img = get_mask_from_gray(img, upper_val=100)
lg.info(f"load image {img.shape}")

lines_arr = get_lines(get_mask_from_gray(img).copy())
complete = islands_from_lines(lines_arr)
lg.info(f"get islands {len(complete)}")

# with open("test.dt", mode="wb") as f:
#   pickle.dump(complete, f, protocol=pickle.HIGHEST_PROTOCOL)

# with open("test.dt", mode="rb") as f:
#   complete = pickle.load(f)

isl = draw_islands(complete, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))

imwrite(PATH_TO_OUTPUT_ + "islands.png", isl)
lg.info(f"fin")
