import lpips

from comparison_list import ComparisonList
from edit_grid import EditGrid
from load_images import load_images_multi_thread
from lpips_runner import LpipsRunner
from utils import get_image_paths


class Controller:

    def __init__(self):
        self.edit_grid = EditGrid()
        self.comparison_list = ComparisonList()

        self.dataset_images_paths = None
        self.comparison_images_paths = None

        self.dataset_images = None

        self.current_index = 0

        self.lpips_runner = LpipsRunner(True)

    def load_dataset(self, dir_path):
        self.dataset_images_paths = get_image_paths(dir_path)
        self.dataset_images = load_images_multi_thread(self.dataset_images_paths, 4)
        assert len(self.dataset_images) > 0
        self.edit_grid.set_image(self.dataset_images[self.current_index])

    def load_comparison_images(self, dir_path):
        self.comparison_images_paths = get_image_paths(dir_path)
        comparison_images = load_images_multi_thread(self.comparison_images_paths, 4)
        assert len(comparison_images) > 0
        self.comparison_list.set_images(comparison_images)

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.dataset_images):
            self.edit_grid.set_image(self.dataset_images[self.current_index])
        else:
            print('No more images to process.')

    def run_lpips(self):
        if len(self.edit_grid.computed_images) > 0 and len(self.comparison_list.images) > 0:
            for i in range(len(self.edit_grid.computed_images)):
                img0 = self.edit_grid.computed_images[i]
                sum_values = 0.0
                for img1 in self.comparison_list.images:
                    sum_values += self.lpips_runner.eval(img0, img1)
                average = sum_values / len(self.comparison_list.images)
                self.edit_grid.scores[i].setText(f"{average:.4f}")
