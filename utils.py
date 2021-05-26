import os

import numpy as np


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
