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
