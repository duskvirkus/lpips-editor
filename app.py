import sys

import cv2
import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.image_frame = QtWidgets.QLabel()
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

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(open_ref_image_action)
        toolbar.addAction(open_dataset_action)
        toolbar.addAction(exit_action)

        self.setCentralWidget(self.image_frame)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def open_ref_image(self):
        reference_image = QFileDialog.getOpenFileName(self, 'Open Reference Image', '~', "Image files (*.jpg *.png)")
        editor.set_ref_image(reference_image[0])
        self.show_ref_image()

    def open_dataset(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Dataset')
        editor.set_dataset_dir(dir_name)

    def show_ref_image(self):
        ref_img = editor.ref_image;
        ref_image_display = QtGui.QImage(
            ref_img.data,
            ref_img.shape[1],
            ref_img.shape[0],
            QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(ref_image_display))


class Editor:

    def __init__(self):
        self.ref_image = None
        self.dataset_dir = ''

        self.image_list_index = 0
        self.image_list = None
        self.current_image = None

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
            self.current_image = cv2.imread(self.image_list[self.image_list_index])
            self.image_list_index += 1
        else:
            print('no more images in directory')


def main():
    global editor
    editor = Editor()

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
