from comparison_list import ComparisonList
from edit_grid import EditGrid
from utils import get_image_paths


class Controller:

    def __init__(self):
        # self.ref_image = create_blank(1024, 1024, rgb_color=(0, 255, 0))
        # self.dataset_dir = ''
        #
        # self.image_list_index = 0
        # self.image_list = None
        # self.current_image = create_blank(1024, 1024, rgb_color=(255, 0, 0))

        self.edit_grid = EditGrid()
        self.comparison_list = ComparisonList()

        self.dataset_images_paths = None
        self.comparison_images_paths = None

        self.dataset_images = None
        self.comparison_images = None

    def load_dataset(self, dir_path):
        self.dataset_images_paths = get_image_paths(dir_path)

    def load_comparison_images(self, dir_path):
        self.comparison_images_paths = get_image_paths(dir_path)

    # def set_ref_image(self, path):
    #     self.ref_image = cv2.imread(path)
    #     print(path)
    #     # print(self.ref_image)
    #
    # def set_dataset_dir(self, dir_name):
    #     self.dataset_dir = dir_name
    #     self.create_image_list()
    #
    # def create_image_list(self):
    #
    #
    # def load_next_image(self):
    #     if self.image_list_index < len(self.image_list):
    #         # self.current_image = cv2.imread(self.image_list[self.image_list_index])
    #         edit_grid.set_image(self.image_list[self.image_list_index])
    #         self.image_list_index += 1
    #     else:
    #         print('no more images in directory')
