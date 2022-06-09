import datetime
import statistics

import numpy
from PIL import Image
from numpy import array

from conversion_functions import image_cutter, rgb_to_grid, photos_to_digits
from main import RemoveOverlay

# imgs = array(rgb_to_grid(image_cutter('photos/mother.jpg', 5, 5, 10, 3)), dtype='int64')
# print(imgs.shape)
# classsss = RemoveOverlay(imgs.shape[2], imgs.shape[3], imgs)
# probs = classsss.probability_finder((0, 0), (0, 1), 'x')
# print(classsss.x_y_finder())
imgs = array(rgb_to_grid(photos_to_digits('images')), dtype='int64')
a = datetime.datetime.now()
classsss = RemoveOverlay(imgs.shape[2], imgs.shape[3], imgs)
xs, ys = [], []
for i in range(20):
    x, y = classsss.x_y_finder()
    xs.append(x)
    ys.append(y)
print(xs)
print(ys)
print(statistics.mode(xs))
print(statistics.mode(ys))

