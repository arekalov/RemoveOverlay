import datetime
import statistics

import numpy
from PIL import Image
from numpy import array

from conversion_functions import image_cutter, rgb_to_grid, photos_to_digits
from main import RemoveOverlay

remover = RemoveOverlay('images')
for i in range(15):
    print(remover.x_y_finder())