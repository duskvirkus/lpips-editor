import sys

import cv2
import os
import numpy as np

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


def main():

    controller = Controller()

    app = QApplication(sys.argv)
    ex = Window(controller)
    sys.exit(app.exec_())

    # global editor
    # editor = Conroller()
    #
    # global edit_grid
    # edit_grid = EditGrid()
    #
    #
    # ex = GUI()



if __name__ == '__main__':
    main()
