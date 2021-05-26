import cv2
from PyQt5 import QtWidgets, QtGui


class ComparisonList:

    def __init__(self):
        self.images = []

        self.comparison_v_layout = None
        self.comparison_frames = None

    def create_q_widgets(self):
        self.comparison_v_layout = QtWidgets.QVBoxLayout()
        self.comparison_frames = []
        comparison_count = 10
        for i in range(comparison_count):
            self.comparison_frames.append(QtWidgets.QLabel())
            self.comparison_v_layout.addWidget(self.comparison_frames[-1])

    def set_parent(self, parent):
        parent.addLayout(self.comparison_v_layout)

    def set_images(self, images):
        self.images = images
        self.update_images()

    def update_images(self):
        if len(self.images) > 0:
            loop_num = len(self.comparison_frames)
            if loop_num > len(self.images):
                loop_num = len(self.images)
            for i in range(loop_num):
                img = self.images[i]
                size = 64
                img = cv2.resize(img, (size, size))
                img_display = QtGui.QImage(
                    img.data,
                    img.shape[1],
                    img.shape[0],
                    QtGui.QImage.Format_RGB888
                ).rgbSwapped()
                self.comparison_frames[i].setPixmap(QtGui.QPixmap.fromImage(img_display))
