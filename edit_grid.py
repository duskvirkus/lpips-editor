import cv2
from PyQt5 import QtWidgets, QtGui, QtCore

from utils import create_blank_image


class EditGrid:

    def __init__(self, controller):
        self.controller = controller

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

    def set_grid_parent(self, parent):
        parent.addLayout(self.q_grid)
        self.compute_images()
        self.update_display()

    def compute_images(self):
        for i in range(self.x_dim()):
            for j in range(self.y_dim()):
                if i == self.x_neg_dim and j == self.y_neg_dim:
                    self.computed_images[self.index(i, j)] = self.image
                else:
                    # TODO compute images
                    self.computed_images[self.index(i, j)] = self.image
        self.controller.run_lpips()

    def update_display(self):
        img = self.image
        size = 100
        img = cv2.resize(img, (size, size))
        img_display = QtGui.QImage(
            img.data,
            img.shape[1],
            img.shape[0],
            QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        for i in range(len(self.q_widgets)):
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
