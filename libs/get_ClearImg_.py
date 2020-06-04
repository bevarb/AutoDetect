import cv2
import os
from PIL import Image
import numpy as np
from PyQt5.QtCore import *
class get_ClearImg(QThread):

    progressBarValue = pyqtSignal(int)
    def __init__(self, source_dir, save_dir, method, T, Step, parent=None):
        super(get_ClearImg, self).__init__()
        self.source_dir = source_dir
        self.save_dir = save_dir
        self.method = method
        self.T = T
        self.Step = Step
        self.quick_flag = 0
    def __del__(self):
        self.wait()

    def run(self):
        root = self.source_dir
        name = os.listdir(root)
        # name = sorted(name, key=lambda x: int(x.split("_")[1]))
        name = sorted(name, key=lambda x: int(x.split("_")[-1].split(".")[0]))
        path = [root + "/" + na for na in name]
        flag = 0
        for i in range(0, len(path) - 1, self.Step):
            n = i // self.T

            # img1 = np.array(Image.open(path[n * 500]))
            # img2 = np.array(Image.open(path[i + 1]))
            img1 = cv2.imread(path[n * self.T])
            img2 = cv2.imread(path[i + 1])
            img = img2 - img1

            img = cv2.bitwise_not(img)

            cv2.imwrite(self.save_dir+"/%d.tif" % (i + 1), img)
            flag += 1
            if self.quick_flag == 1:
                break
            prograssbar_value = round(flag / (len(path) - 1), 2) * 100
            self.progressBarValue[int].emit(int(prograssbar_value))
            print(self.T, i)

    def set_quick_flag(self, i):
        self.quick_flag = i



