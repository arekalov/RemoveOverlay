import datetime
import statistics
import numpy
from PIL import Image
from conversion_functions import image_cutter, rgb_to_grid, photos_to_digits
from main import RemoveOverlay


remover = RemoveOverlay('images')
a = datetime.datetime.now()
print(remover.x_y_finder())
b = datetime.datetime.now()
print(b-a)