import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize

from transformations import TransformationPicker, compute_images, ComputeImageData
from utils import create_blank_image, map_value


class EditGrid:

    def __init__(self):
        self.image = create_blank_image(1024, 1024, rgb_color=(0, 0, 255))

        initial_dim = 2
        self.x_pos_dim = initial_dim
        self.x_neg_dim = initial_dim
        self.y_pos_dim = initial_dim
        self.y_neg_dim = initial_dim

        self.computed_images = None
        self.init_computed_images()

        self.q_grid = QtWidgets.QGridLayout()
        self.q_widgets = None

        self.scores = None

        self.transformation_panel = None
        self.x_offset_container = None
        self.x_offset = None
        self.y_offset_container = None
        self.y_offset = None
        self.x_transformation_picker = None
        self.y_transformation_picker = None

        self.initialized = False

    def init_computed_images(self):
        self.computed_images = []
        for i in range(self.x_dim() * self.y_dim()):
            self.computed_images.append(None)

    def create_q_widgets(self):
        self.q_widgets = []
        self.scores = []
        for i in range(self.x_dim() * self.y_dim()):
            self.q_widgets.append(QtWidgets.QLabel())
            self.q_grid.addWidget(
                self.q_widgets[-1],
                (i // self.x_dim()) * 2,
                i % self.x_dim(),
                QtCore.Qt.AlignCenter
            )

            self.scores.append(QtWidgets.QLabel('-'))
            self.q_grid.addWidget(
                self.scores[-1],
                (i // self.x_dim()) * 2 + 1,
                i % self.x_dim(),
                QtCore.Qt.AlignCenter
            )

        self.transformation_panel = QtWidgets.QVBoxLayout()

        self.x_offset_container = QtWidgets.QHBoxLayout()
        x_offset_l = QtWidgets.QLabel('x offset')
        self.x_offset = QtWidgets.QDoubleSpinBox()
        self.x_offset.setRange(-1, 1)
        self.x_offset.setSingleStep(0.05)
        self.x_offset_container.addWidget(x_offset_l)
        self.x_offset_container.addWidget(self.x_offset)
        self.transformation_panel.addLayout(self.x_offset_container)

        self.y_offset_container = QtWidgets.QHBoxLayout()
        y_offset_l = QtWidgets.QLabel('y offset')
        self.y_offset = QtWidgets.QDoubleSpinBox()
        self.y_offset.setRange(-1, 1)
        self.y_offset.setSingleStep(0.05)
        self.y_offset_container.addWidget(y_offset_l)
        self.y_offset_container.addWidget(self.y_offset)
        self.transformation_panel.addLayout(self.y_offset_container)

        self.x_transformation_picker = TransformationPicker(self, self.transformation_panel, 'x transformation')
        self.y_transformation_picker = TransformationPicker(self, self.transformation_panel, 'y transformation')

        self.initialized = True

    def set_grid_parent(self, parent):
        parent.addLayout(self.transformation_panel)
        parent.addLayout(self.q_grid)
        self.compute_images()
        self.update_display()

    def update(self):
        if self.initialized:
            self.compute_images()
            self.update_display()

    def compute_images(self):
        # for i in range(self.x_dim()):
        #     for j in range(self.y_dim()):
        #         if i == self.x_neg_dim and j == self.y_neg_dim:
        #             self.computed_images[self.index(i, j)] = self.image
        #         else:
        #             # TODO compute images
        #             self.computed_images[self.index(i, j)] = self.image
        #
        locations = []
        for i in range(self.x_dim() * self.y_dim()):
            locations.append((
                map_value(i // self.x_dim(), 0, self.x_dim(), -1, 1),
                map_value(i % self.x_dim(), 0, self.y_dim(), -1, 1)
            ))

        data = ComputeImageData(
            self.image,
            locations,
            self.x_transformation_picker.transformer,
            self.y_transformation_picker.transformer,
            4
        )
        self.computed_images = compute_images(data)

    def update_display(self):
        for i in range(len(self.computed_images)):
            img = self.computed_images[i].copy()
            size = 100
            img = cv2.resize(img, (size, size))
            img_display = QtGui.QImage(
                img.data,
                img.shape[1],
                img.shape[0],
                QtGui.QImage.Format_RGB888
            ).rgbSwapped()
            self.q_widgets[i].setPixmap(QtGui.QPixmap.fromImage(img_display))

    def set_image(self, img):
        self.image = img
        self.compute_images()
        self.update_display()

    def index(self, x, y):
        return x + y * self.x_dim()

    def x_dim(self):
        return 1 + self.x_pos_dim + self.x_neg_dim

    def y_dim(self):
        return 1 + self.y_pos_dim + self.y_neg_dim
