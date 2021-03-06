from libs.detect.yolo4.yolo import *
import numpy as np
import os
import cv2
from libs.pascal_voc_io import PascalVocWriter
from PyQt5.QtCore import *
from PIL import Image
# 首先下载模型文件https://s3.ap-northeast-2.amazonaws.com/open-mmlab/mmdetection/models/faster_rcnn_r50_fpn_1x_20181010-3d1b3351.pth
class yolo_detect(QThread):
    progressBarValue = pyqtSignal(int)

    def __init__(self, model_path, config_path, defaultSaveDir, dirname, score, is_search_central, gamma, parent=None):
        super(yolo_detect, self).__init__()
        config_file = config_path
        checkpoint_file = model_path
        # 初始化模型
        _defaults = {
            "model_path": model_path,
            "anchors_path": 'libs/detect/yolo4/model_data/yolo_anchors.txt',
            "classes_path": 'libs/detect/yolo4/model_data/voc_classes.txt',
            "model_image_size": (416, 416, 3),
            "confidence": 0.5,
            "cuda": True
        }
        self.is_search_central = is_search_central
        self.gamma = gamma
        if self.gamma == -1:
            print("读取info文件中的gamma,最好再发送一个信号")
        print(self.gamma)
        self.yolo4 = YOLO(_defaults)
        self.defaultSaveDir = defaultSaveDir
        self.dirname = dirname
        self.score = score
        self.quick_flag = 0
        self.classes = ["binding", "debinding"]
        self.central_intensity = []
    def __del__(self):
        self.wait()

    def run(self):
        # 测试一张图片
        dirname = self.dirname
        imgs = os.listdir(dirname)
        if imgs is not None:
            img_paths = sorted(imgs, key=lambda x: int(x.split('/')[-1].split('.')[0]))
            img_size = cv2.imread(dirname + "/" + imgs[0]).shape
            flag = 0
            for img_path in img_paths:
                # print(img_path)
                path = dirname + "/" + img_path
                id = img_path.split('.')[0]

                img = Image.open(path)
                # low_img = np.array(img).astype(np.uint8)
                low_img = cv2.imread(path)
                image = Image.fromarray(low_img)
                # print(np.array(image).dtype)
                bboxs = self.yolo4.detect_image(image)
                # print(bboxs)
                # 寻找最大值
                if self.is_search_central == 1:
                    newbboxs = self.search_central(img, bboxs)
                else:
                    newbboxs = bboxs
                filename = id + ".tif"
                xmlwriter = PascalVocWriter("VOC2007", filename, img_size)
                for box in newbboxs:
                    intensity = self.get_intensity(img, box)  # 获取强度值
                    xmlwriter.addBndBox(box[0], box[1], box[2], box[3], self.classes[int(box[-1])], "0", intensity)
                xmlwriter.save(self.defaultSaveDir + "/" + id + ".xml")
                flag += 1
                if self.quick_flag == 1:
                    break
                prograssbar_value = round(flag / len(imgs), 2) * 100
                self.progressBarValue[int].emit(int(prograssbar_value))

    def set_quick_flag(self, i):
        self.quick_flag = i

    def get_intensity(self, img, box):
        '''获取中心强度值，并不是直接读取，而是根据预处理反过来到原来的数据'''
        img = np.array(img)
        central_x, central_y = int((box[1] + box[3]) / 2), int((box[0] + box[2]) / 2)
        L = 2
        x_min, y_min, x_max, y_max = central_x - L, central_y - L, central_x + L, central_y + L
        data = img[x_min:x_max, y_min:y_max].astype(np.int32)
        # print(data)
        score = 32500
        data = data - score
        # print(data)
        data[data[:, :] < 0] = (-1) * np.power(np.abs(data[data[:, :] < 0]) / score, 1 / self.gamma) * score
        data[data[:, :] > 0] = np.power(np.abs(data[data[:, :] > 0]) / score, 1 / self.gamma) * score
        # print(data)
        data = data / 2  #
        intensity = np.mean(data)  # 获取均值
        return intensity

    def search_central(self, img, bboxs):
        '''对检测后的数据寻找最亮点或者最暗点，然后再根据这个点生成新的标准框'''
        img = np.array(img)
        shape = img.shape
        new_bboxs = []
        for bbox in bboxs:
            index = []
            win = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
            if bbox[-1] == 0:
                index = np.where(win == np.max(win))
            elif bbox[-1] == 1:
                index = np.where(win == np.min(win))
            if index[0].shape[0] > 1:
                index = [index[0][0], index[1][0]]
            c_x, c_y = int(bbox[0] + index[1]), int(bbox[1] + index[0])

            begain_x, begain_y, over_x, over_y = c_x - 10, c_y - 10, c_x + 10, c_y + 10
            newbbox = np.array([begain_x, begain_y, over_x, over_y, bbox[-1]])
            newbbox[newbbox[:] < 0] = 0
            newbbox[2] = shape[0] if newbbox[2] > shape[0] else newbbox[2]
            newbbox[3] = shape[1] if newbbox[3] > shape[1] else newbbox[3]
            new_bboxs.append(newbbox)

        return new_bboxs