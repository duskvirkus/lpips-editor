from comparison_list import ComparisonList
from edit_grid import EditGrid
from load_images import load_images_multi_thread
from utils import get_image_paths


class Controller:

    def __init__(self):
        self.edit_grid = EditGrid()
        self.comparison_list = ComparisonList()

        self.dataset_images_paths = None
        self.comparison_images_paths = None

        self.dataset_images = None
        self.comparison_images = None

        self.current_index = 0

    def load_dataset(self, dir_path):
        self.dataset_images_paths = get_image_paths(dir_path)
        self.dataset_images = load_images_multi_thread(self.dataset_images_paths, 4)
        assert len(self.dataset_images) > 0
        self.edit_grid.set_image(self.dataset_images[self.current_index])

    def load_comparison_images(self, dir_path):
        self.comparison_images_paths = get_image_paths(dir_path)
        self.comparison_images = load_images_multi_thread(self.comparison_images_paths, 4)
        assert len(self.comparison_images) > 0
        self.comparison_list.set_images(self.comparison_images)

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.dataset_images):
            self.edit_grid.set_image(self.dataset_images[self.current_index])
        else:
            print('No more images to process.')
