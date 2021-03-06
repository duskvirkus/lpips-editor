import os
import queue
import threading
import time

import cv2


def load_images(dir_path, thread_count=1, verbose=False):
    paths = []
    for root, subdirs, files in os.walk(dir_path):
        if verbose:
            print('--\nroot = ' + root)
        for subdir in subdirs:
            if verbose:
                print('\t- subdirectory ' + subdir)
        for filename in files:
            file_path = os.path.join(root, filename)
            paths.append(file_path)
    return load_images_multi_thread(paths, thread_count, verbose)


def load_images_multi_thread(paths, thread_count=1, verbose=False):
    paths_len = len(paths)
    data = LoadData(paths, verbose)
    threads = []

    for i in range(thread_count):
        threads.append(ImageLoaderThread(i, 'image_load_thread_' + str(i), data))
        threads[-1].start()

    while not data.paths_queue.empty():
        pass

    timeout_count = 1000
    while len(data.images) != paths_len and timeout_count > 0:
        time.sleep(1)
        timeout_count -= 1

    data.exit_flag = True

    return data.images


class LoadData:

    def __init__(self, paths, verbose):
        self.verbose = verbose
        self.lock = threading.Lock()
        self.exit_flag = False
        self.images = []

        self.lock.acquire()
        self.paths_queue = queue.Queue()
        for path in paths:
            self.paths_queue.put(path)
        self.lock.release()


class ImageLoaderThread(threading.Thread):
    def __init__(self, thread_id, name, data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.data = data

    def run(self):
        load_image(self.name, self.data)


def load_image(thread_name, data):
    while not data.exit_flag:
        path = None
        data.lock.acquire()
        if not data.paths_queue.empty():
            path = data.paths_queue.get()
        data.lock.release()
        if path is not None:
            img = cv2.imread(path)
            if img is not None:
                data.lock.acquire()
                data.images.append(img)
                data.lock.release()
                if data.verbose:
                    print(thread_name + " loaded " + path + " successfully.")
            else:
                print("Warning! Image not loaded at path: " + path)
