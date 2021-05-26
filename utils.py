import os

import numpy as np
from scipy.interpolate import interp1d


def create_blank_image(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image


def get_image_paths(dir_path):
    paths = []
    for root, subdirs, files in os.walk(dir_path):
        for filename in files:
            paths.append(root + '/' + filename)
    return paths


def map_value(val: float, min1, max1, min2, max2) -> float:
    m = interp1d([min1, max1], [min2, max2])
    return float(m(val))

