from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QCheckBox


class Window(QMainWindow):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        # setup actions
        open_comparison_dir_action = QAction('Open Comparison Images Directory', self)
        open_comparison_dir_action.setShortcut('Ctrl+O')
        open_comparison_dir_action.setStatusTip('Open a folder of comparison images.')
        open_comparison_dir_action.triggered.connect(self.open_comparison_dir)

        open_dataset_action = QAction('Open Dataset', self)
        open_dataset_action.setShortcut('Ctrl+D')
        open_dataset_action.setStatusTip('Open a folder of images to work on.')
        open_dataset_action.triggered.connect(self.open_dataset)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        # setup gui elements
        self.core_widget = QtWidgets.QWidget()
        self.core_v_layout = QtWidgets.QVBoxLayout()
        self.core_widget.setLayout(self.core_v_layout)

        self.secondary_h_layout = QtWidgets.QHBoxLayout()
        self.secondary_h_layout.addStretch(0)
        self.core_v_layout.addLayout(self.secondary_h_layout)

        self.navigation = QtWidgets.QHBoxLayout()

        self.use_gpu_checkbox = QCheckBox('Use GPU')
        self.use_gpu_checkbox.setChecked(True)
        self.navigation.addWidget(self.use_gpu_checkbox)

        self.next_image = QtWidgets.QPushButton('Next Image')
        self.next_image.clicked.connect(self.next_image_func)
        self.navigation.addWidget(self.next_image)

        self.core_v_layout.addLayout(self.navigation)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_comparison_dir_action)
        file_menu.addAction(open_dataset_action)
        file_menu.addAction(exit_action)

        # setup edit grid and comparison list
        self.controller.edit_grid.create_q_widgets()
        self.controller.edit_grid.set_grid_parent(self.secondary_h_layout)
        self.controller.comparison_list.create_q_widgets()
        self.controller.comparison_list.set_parent(self.secondary_h_layout)

        # finish setting up gui
        self.setCentralWidget(self.core_widget)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Main window')
        self.show()

    def open_comparison_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Comparison Images Directory')
        self.controller.load_comparison_images(dir_name)

    def open_dataset(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Dataset')
        self.controller.load_dataset(dir_name)

    def next_image_func(self):
        self.controller.next_image()
