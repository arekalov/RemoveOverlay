import datetime
import os
import statistics
import numpy
from PIL import Image

from RemoveOverlay import RemoveOverlay

remover = RemoveOverlay('images')
biases = remover.x_y_finder()
remover.cut_and_sew('new1.jpg', biases)