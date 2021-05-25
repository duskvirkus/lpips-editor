import sys

import cv2
import os
import numpy as np

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.core_widget = QtWidgets.QWidget()
        self.core_v_layout = QtWidgets.QVBoxLayout()
        self.core_widget.setLayout(self.core_v_layout)

        self.secondary_h_layout = QtWidgets.QHBoxLayout()
        self.secondary_h_layout.addStretch(1)
        self.core_v_layout.addLayout(self.secondary_h_layout)

        self.navigation = QtWidgets.QHBoxLayout()
        self.next_image = QtWidgets.QPushButton('Next Image')
        self.navigation.addWidget(self.next_image)
        self.core_v_layout.addLayout(self.navigation)

        self.comparison_scroll = QtWidgets.QScrollArea()
        self.secondary_h_layout.addWidget(self.comparison_scroll)
        self.comparison_v_layout = QtWidgets.QVBoxLayout(self.comparison_scroll)
        self.comparison_frames = []
        comparison_count = 10
        for i in range(comparison_count):
            self.comparison_frames.append(QtWidgets.QLabel())
            self.comparison_v_layout.addWidget(self.comparison_frames[-1])
        self.update_comparison_images()

        # self.editor_grid = QtWidgets.QGridLayout()
        # self.editor_image_frames = []
        # editor_images_dim = 7
        # for i in range(editor_images_dim * editor_images_dim):
        #     self.editor_image_frames.append(QtWidgets.QLabel())
        #     self.editor_grid.addWidget(
        #         self.editor_image_frames[-1],
        #         i // editor_images_dim,
        #         i % editor_images_dim,
        #         Qt.AlignCenter
        #     )
        # self.update_editor_images()
        # self.secondary_h_layout.addLayout(self.editor_grid)
        edit_grid.create_q_widgets()
        edit_grid.set_grid_parent(self.secondary_h_layout)

        self.init_ui()

    def init_ui(self):

        open_ref_image_action = QAction(QIcon('open24.png'), 'Open Reference Image', self)
        open_ref_image_action.setShortcut('Ctrl+O')
        open_ref_image_action.setStatusTip('Opens a file')
        open_ref_image_action.triggered.connect(self.open_ref_image)

        open_dataset_action = QAction(QIcon('opendir24.png'), 'Open Dataset', self)
        open_dataset_action.setShortcut('Ctrl+D')
        open_dataset_action.setStatusTip('Open a folder of images to work on.')
        open_dataset_action.triggered.connect(self.open_dataset)

        exit_action = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_ref_image_action)
        file_menu.addAction(open_dataset_action)
        file_menu.addAction(exit_action)

        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(open_ref_image_action)
        # toolbar.addAction(open_dataset_action)
        # toolbar.addAction(exit_action)

        self.setCentralWidget(self.core_widget)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Main window')
        self.show()

    def open_ref_image(self):
        reference_image = QFileDialog.getOpenFileName(self, 'Open Reference Image', '~', "Image files (*.jpg *.png)")
        editor.set_ref_image(reference_image[0])
        self.update_comparison_images()

    def open_dataset(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Dataset')
        editor.set_dataset_dir(dir_name)
        # self.update_editor_images()

    def update_comparison_images(self):
        img = editor.ref_image
        size = 64
        img = cv2.resize(img, (size, size))
        img_display = QtGui.QImage(
            img.data,
            img.shape[1],
            img.shape[0],
            QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        for i in range(len(self.comparison_frames)):
            self.comparison_frames[i].setPixmap(QtGui.QPixmap.fromImage(img_display))

    def update_editor_images(self):
        img = editor.current_image
        size = 100
        img = cv2.resize(img, (size, size))
        img_display = QtGui.QImage(
            img.data,
            img.shape[1],
            img.shape[0],
            QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        for i in range(len(self.editor_image_frames)):
            self.editor_image_frames[i].setPixmap(QtGui.QPixmap.fromImage(img_display))


class EditGrid:

    def __init__(self):
        self.image = create_blank(1024, 1024, rgb_color=(0, 0, 255))

        initial_dim = 3
        self.x_pos_dim = initial_dim
        self.x_neg_dim = initial_dim
        self.y_pos_dim = initial_dim
        self.y_neg_dim = initial_dim

        self.computed_image = None
        self.init_computed_images()

        self.q_grid = QtWidgets.QGridLayout()
        self.q_widgets = None

    def init_computed_images(self):
        self.computed_image = []
        for i in range(self.x_dim() * self.y_dim()):
            self.computed_image.append(None)

    def create_q_widgets(self):
        self.q_widgets = []
        for i in range(self.x_dim() * self.y_dim()):
            self.q_widgets.append(QtWidgets.QLabel())
            self.q_grid.addWidget(
                self.q_widgets[-1],
                i // self.x_dim(),
                i % self.x_dim(),
                Qt.AlignCenter
            )

    def set_grid_parent(self, parent):
        parent.addLayout(self.q_grid)
        self.compute_images()
        self.update_display()

    def compute_images(self):
        for i in range(self.x_dim()):
            for j in range(self.y_dim()):
                if i == self.x_neg_dim and j == self.y_neg_dim:
                    self.computed_image[self.index(i, j)] = self.image
                else:
                    # TODO compute images
                    self.computed_image[self.index(i, j)] = self.image

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

    def set_image(self, path):
        self.image = cv2.imread(path)
        self.compute_images()
        self.update_display()

    def index(self, x, y):
        return x + y * self.x_dim()

    def x_dim(self):
        return 1 + self.x_pos_dim + self.x_neg_dim

    def y_dim(self):
        return 1 + self.y_pos_dim + self.y_neg_dim


class Editor:

    def __init__(self):
        self.ref_image = create_blank(1024, 1024, rgb_color=(0, 255, 0))
        self.dataset_dir = ''

        self.image_list_index = 0
        self.image_list = None
        self.current_image = create_blank(1024, 1024, rgb_color=(255, 0, 0))

    def set_ref_image(self, path):
        self.ref_image = cv2.imread(path)
        print(path)
        # print(self.ref_image)

    def set_dataset_dir(self, dir_name):
        self.dataset_dir = dir_name
        self.create_image_list()

    def create_image_list(self):
        images = []
        for root, subdirs, files in os.walk(self.dataset_dir):
            for filename in files:
                images.append(root + '/' + filename)
        self.image_list = images
        self.load_next_image()

    def load_next_image(self):
        if self.image_list_index < len(self.image_list):
            # self.current_image = cv2.imread(self.image_list[self.image_list_index])
            edit_grid.set_image(self.image_list[self.image_list_index])
            self.image_list_index += 1
        else:
            print('no more images in directory')


def main():
    global editor
    editor = Editor()

    global edit_grid
    edit_grid = EditGrid()

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
