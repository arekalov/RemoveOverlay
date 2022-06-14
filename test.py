import datetime
import os
import statistics
import numpy
from PIL import Image

from main import RemoveOverlay

remover = RemoveOverlay('images')
biases = remover.x_y_finder()
print(biases)
remover.cut_and_sew('new.jpg', biases)