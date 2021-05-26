import sys

import cv2
import os
import numpy as np

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap

from controller import Controller
from window import Window


def main():

    controller = Controller()

    app = QApplication(sys.argv)
    ex = Window(controller)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
