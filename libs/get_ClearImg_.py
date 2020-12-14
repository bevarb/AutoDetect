import cv2
import os
from PIL import Image
import numpy as np
from PyQt5.QtCore import *
class get_ClearImg(QThread):

    progressBarValue = pyqtSignal(int)
    over_Sig = pyqtSignal(int)
    def __init__(self, source_dir, save_dir, method, T, Step, mean_Step, gama,
                 is_mean=0, is_32Bit=0, is_reverse=0, Flag="_", Num="-1", parent=None):
        super(get_ClearImg, self).__init__()
        self.source_dir = source_dir
        self.save_dir = save_dir
        self.method = method
        self.T = T
        self.gama = gama
        self.Step = Step
        self.mean_Step = mean_Step
        self.Flag = Flag
        self.Num = Num
        self.quick_flag = 0
        self.is_mean = is_mean
        self.is_32Bit = is_32Bit
        self.is_reverse = is_reverse
        # 添加保存信息的文件
        self.save_info()

    def save_info(self):
        path = self.save_dir.split("/")
        dir = "/".join(path[0: len(path) - 1])

        file_path = dir + "/info.txt"
        f = open(file_path, "a")
        info = "\n".join(["Source Dir: %s" % self.source_dir,
                          "Save Dir: %s" % self.save_dir,
                          "Method(0->Sub First, 1-> Sub Pre): %d" % self.method,
                          "T: %d" % self.T,
                          "Gamma: %d" % self.gama,
                          "Step: %d" % self.Step,
                          "Mean Step: %d" % self.mean_Step,
                          "Flag(For Split IMG's path ): %s" % self.Flag,
                          "Num(For Split IMG's path ): %s" % self.Num,
                          "Is Mean: %d" % self.is_mean,
                          "Is 32Bit: %d" % self.is_32Bit,
                          "Is Reverse: %d" % self.is_reverse])
        f.write(info)
        f.close()
        print("Have write info to %s" % dir)
    def __del__(self):
        self.wait()

    def run(self):
        root = self.source_dir
        name = os.listdir(root)
        def file_filter(f):
            if f.endswith(".tif"):
                return True
            else:
                return False
        name = list(filter(file_filter, name))
        # name = sorted(name, key=lambda x: int(x.split("_")[1]))
        if len(self.Flag) == 1:
            name = sorted(name, key=lambda x: int(x.split(self.Flag)[int(self.Num)]))
        elif len(self.Flag) == 2:
            name = sorted(name, key=lambda x: int(x.split(self.Flag[0])[int(self.Num[0])].split(self.Flag[1])[int(self.Num[1])]))
        path = [root + "/" + na for na in name]
        flag = 0
        for i in range(0, len(path) - 2 * max(self.Step, self.mean_Step), self.Step):
            n = i // self.T
            if self.is_32Bit == True:
                if self.is_mean == 0:
                    img1 = np.array(Image.open(path[n * self.T]))
                    img2 = np.array(Image.open(path[i + self.Step]))
                else:
                    img1 = np.array(Image.open(path[n * self.T])) // self.mean_Step
                    img2 = np.array(Image.open(path[i + self.Step])) // self.mean_Step
                    for k in range(1, self.mean_Step):
                        img1 += np.array(Image.open(path[n * self.T + k])) // self.mean_Step
                        img2 += np.array(Image.open(path[i + self.Step + k])) // self.mean_Step
                img1 = img1.astype(np.int32)
                img2 = img2.astype(np.int32)
            else:
                if self.is_mean == 0:
                    img1 = cv2.imread(path[n * self.T])
                    img2 = cv2.imread(path[i + 1])
                else:
                    img1 = np.array(Image.open(path[n * self.T])) // self.mean_Step
                    img2 = np.array(Image.open(path[i + self.Step])) // self.mean_Step
                    for k in range(1, self.mean_Step):
                        img1 += np.array(Image.open(path[n * self.T + k])) // self.mean_Step
                        img2 += np.array(Image.open(path[i + self.Step + k])) // self.mean_Step
                img1 = img1.astype(np.uint8)
                img2 = img2.astype(np.uint8)
            img = img2 - img1
            if self.is_32Bit == 1:
                # img = np.abs(img)
                # img = img * (65535 / np.max(img))
                img = self.pretreat(img)
                # img = self.GaussianLowFilter(img, 150)
                # img = cv2.GaussianBlur(img, (3, 3), sigmaX=15)
                img = img.astype(np.uint16)
            if self.is_reverse == 1:
                img = cv2.bitwise_not(img)

            cv2.imwrite(self.save_dir+"/%d.tif" % (i + 1), img)
            # # 这里需要再修改，将16进制转为8进制
            # img = cv2.imread(self.save_dir+"/%d.tif" % (i + 1))
            # cv2.imwrite(self.save_dir + "/%d.tif" % (i + 1), img)

            flag += 1
            if self.quick_flag == 1:
                break
            prograssbar_value = round((flag * self.Step) / (len(path) - 1), 2) * 100
            self.progressBarValue[int].emit(int(prograssbar_value))
            print(self.T, i)
        self.over_Sig[int].emit(1)
    def set_quick_flag(self, i):
        self.quick_flag = i

    def pretreat(self, img):

        img = img - np.mean(img)
        scale = 0.5

        # 放缩
        img = img / scale

        # gamma
        g = self.gama
        score = 32500

        img[img[:, :] < 0] = (-1) * np.power(np.abs(img[img[:, :] < 0]) / score, g) * score
        img[img[:, :] > 0] = np.power(np.abs(img[img[:, :] > 0]) / score, g) * score

        img[img < -score] = -score
        img[img > score] = score

        # 获取基本信息
        img = img + score
        img = img.astype(np.uint16)
        return img

    def GaussianLowFilter(self, image, d):
        f = np.fft.fft2(image)
        fshift = np.fft.fftshift(f)

        def make_transform_matrix(d):
            transfor_matrix = np.zeros(image.shape)
            center_point = tuple(map(lambda x: (x - 1) / 2, fshift.shape))
            for i in range(transfor_matrix.shape[0]):
                for j in range(transfor_matrix.shape[1]):
                    def cal_distance(pa, pb):
                        from math import sqrt
                        dis = sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
                        return dis

                    dis = cal_distance(center_point, (i, j))
                    transfor_matrix[i, j] = np.exp(-(dis ** 2) / (2 * (d ** 2)))
            return transfor_matrix

        d_matrix = make_transform_matrix(d)
        new_img = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift * d_matrix)))
        return new_img


