import queue
import threading
import time
from abc import ABC, abstractmethod, abstractproperty

import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore

import edit_grid
from utils import map_value


class TransformationPicker:

    def __init__(self, edit_grid, parent, name):
        self.edit_grid = edit_grid

        self.dropdown_container = QtWidgets.QHBoxLayout()
        dropdown_l = QtWidgets.QLabel(name)
        self.dropdown = QtWidgets.QComboBox()
        self.dropdown.addItems([cls.__name__ for cls in Transformer.__subclasses__()])
        self.dropdown.currentTextChanged.connect(self.update_transformation)
        self.dropdown_container.addWidget(dropdown_l)
        self.dropdown_container.addWidget(self.dropdown)
        parent.addLayout(self.dropdown_container)

        self.slider_container = QtWidgets.QHBoxLayout()
        slider_label = QtWidgets.QLabel('strength')
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged[int].connect(self.slider_update)
        self.slider_container.addWidget(slider_label)
        self.slider_container.addWidget(self.slider)
        parent.addLayout(self.slider_container)

        self.transformer = None
        self.update_transformation()

    def update_transformation(self):
        cls = globals()[self.dropdown.currentText()]
        self.transformer = cls()

        self.slider.setValue(self.transformer.get_strength())

    def slider_update(self, value):
        self.transformer.set_strength(value)
        self.edit_grid.update()


class Transformer(ABC):

    @abstractmethod
    def get_strength(self) -> float:
        pass

    @abstractmethod
    def set_strength(self, value: float) -> float:
        pass

    @abstractmethod
    def transform_image(self, image: np.ndarray, location: float) -> None:
        pass


class TransformerScale(Transformer):

    def __init__(self):
        self.strength = 50

    def get_strength(self) -> float:
        return self.strength

    def set_strength(self, value: float) -> None:
        self.strength = value

    def transform_image(self, image: np.ndarray, location: float) -> np.ndarray:
        scale = (map_value(self.strength, 0, 100, 0.5, 1.5) + 1) * map_value(location, -1, 1, 0, 1)
        if scale == 0:
            return image.copy()
        out = image.copy()
        start_shape = out.shape
        dim = (int(out.shape[1] * scale), int(out.shape[0] * scale))
        if scale > 1:
            out = cv2.resize(out, dim, interpolation=cv2.INTER_AREA)
            x_crop = (dim[0] - start_shape[1]) // 2
            y_crop = (dim[1] - start_shape[0]) // 2
            out = out[y_crop:dim[1] - y_crop, x_crop:dim[0] - x_crop]
        else:
            out = cv2.resize(out, dim, interpolation=cv2.INTER_AREA)

            pad_x = (start_shape[1] - dim[0]) // 2
            pad_y = (start_shape[0] - dim[1]) // 2

            in_img_h, in_img_w, channels = out.shape
            out_img_h = in_img_h + (pad_y * 2)
            out_img_w = in_img_w + (pad_x * 2)
            mask = np.zeros((out_img_h, out_img_w, 1), np.uint8)
            fill_color = (255, 255, 255)
            out_img = cv2.copyMakeBorder(out, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=fill_color)
            mask = cv2.rectangle(mask, (0, 0), (pad_x - 1, out_img_h - 1), (255), -1)
            mask = cv2.rectangle(mask, (0, 0), (out_img_w - 1, pad_y - 1), (255), -1)
            mask = cv2.rectangle(mask, (0, out_img_h - pad_y), (out_img_w - 1, out_img_h - 1), (255), -1)
            mask = cv2.rectangle(mask, (out_img_w - pad_x, 0), (out_img_w - 1, out_img_h - 1), (255), -1)

            out = cv2.inpaint(out_img, mask, 3, cv2.INPAINT_TELEA)

        if out.shape[1] != 1024 or out.shape[0] != 1024:
            out = cv2.resize(out, (1024, 1024), interpolation=cv2.INTER_AREA)

        return out


class ComputeImageData:

    def __init__(
        self,
        image: np.ndarray,
        locations: [(float, float)],
        transformer_x: Transformer,
        transformer_y: Transformer,
        thread_count: int = 1
    ):
        self.src = image
        self.locations = locations
        self.transformer_x = transformer_x
        self.transformer_y = transformer_y
        self.thread_count = thread_count

        self.output_images = []
        self.exit_flag = False

        self.lock = threading.Lock()
        self.lock.acquire()
        self.index_queue = queue.Queue()
        for i in range(len(self.locations)):
            self.index_queue.put(i)
        # print(list(self.index_queue))

        self.indexes = []
        for i in range(self.thread_count):
            self.indexes.append(-1)

        self.lock.release()


def compute_image(thread_id, data: ComputeImageData) -> None:
    while not data.exit_flag:
        data.indexes[thread_id] = -1
        data.lock.acquire()
        if not data.index_queue.empty():
            data.indexes[thread_id] = data.index_queue.get()
        # print(thread_name + ' working on index ' + str(index))
        data.lock.release()
        if data.indexes[thread_id] < 0 or data.indexes[thread_id] >= len(data.locations):
            break
        else:
            image = data.src
            image = data.transformer_x.transform_image(image, data.locations[data.indexes[thread_id]][1])
            image = data.transformer_y.transform_image(image, data.locations[data.indexes[thread_id]][0])
            if image is not None:
                data.lock.acquire()
                data.output_images.append((data.indexes[thread_id], image))
                data.lock.release()
                # print(thread_name + ' done with index ' + str(index))
            else:
                print("Warning! Something went wrong!")


def compute_images(data: ComputeImageData) -> [np.ndarray]:
    threads = []
    for i in range(data.thread_count):
        threads.append(ComputeImageThread(i, 'compute-image-thread-' + str(i), data))
        threads[-1].start()

    while not data.index_queue.empty():
        pass

    timeout_count = 1000
    while len(data.output_images) != len(data.locations) and timeout_count > 0:
        time.sleep(1)
        timeout_count -= 1

    data.exit_flag = True

    out = []
    for i in range(len(data.output_images)):
        # print(data.output_images[i])
        out.append(None)

    for a in data.output_images:
        out[a[0]] = a[1]

    return out


class ComputeImageThread(threading.Thread):
    def __init__(self, thread_id, name, data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.data = data

    def run(self):
        compute_image(self.thread_id, self.data)
