import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        open_reference_image_action = QAction(QIcon('open24.png'), 'Open Reference Image', self)
        open_reference_image_action.setShortcut('Ctrl+O')
        open_reference_image_action.setStatusTip('Opens a file')
        open_reference_image_action.triggered.connect(self.open_reference_image)

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
        file_menu.addAction(open_reference_image_action)
        file_menu.addAction(open_dataset_action)
        file_menu.addAction(exit_action)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(open_reference_image_action)
        toolbar.addAction(open_dataset_action)
        toolbar.addAction(exit_action)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def open_reference_image(self):
        reference_image = QFileDialog.getOpenFileName(self, 'Open Reference Image', '~', "Image files (*.jpg *.png)")
        print(reference_image)

    def open_dataset(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Dataset')
        print(dir_name)


def main():
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
