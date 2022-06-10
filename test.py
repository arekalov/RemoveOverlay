import datetime
import statistics
import numpy
from PIL import Image
from conversion_functions import image_cutter, rgb_to_grid, photos_to_digits
from main import RemoveOverlay

remover = RemoveOverlay('images')
xs = []
ys = []
for i in range(30):
    print(i)
    x, y = remover.x_y_finder()
    xs.append(x)
    ys.append(y)
print(xs)
print(ys)
print(statistics.mean(xs), statistics.mean(ys))