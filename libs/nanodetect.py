from mmdet.apis import init_detector, inference_detector, show_result
import numpy as np
import os
import cv2
from libs.pascal_voc_io import PascalVocWriter
from PyQt5.QtCore import *
# 首先下载模型文件https://s3.ap-northeast-2.amazonaws.com/open-mmlab/mmdetection/models/faster_rcnn_r50_fpn_1x_20181010-3d1b3351.pth
class detect(QThread):
    progressBarValue = pyqtSignal(int)

    def __init__(self, model_path, config_path, defaultSaveDir, dirname, score, parent=None):
        super(detect, self).__init__()
        config_file = config_path
        checkpoint_file = model_path
        # 初始化模型
        self.model = init_detector(config_file, checkpoint_file)
        self.defaultSaveDir = defaultSaveDir
        self.dirname = dirname
        self.score = score
        self.quick_flag = 0
    def __del__(self):
        self.wait()

    def run(self):
        # 测试一张图片
        dirname = self.dirname
        imgs = os.listdir(dirname)
        if imgs is not None:
            imgs = sorted(imgs, key=lambda x: int(x.split('/')[-1].split('.')[0]))
            img_size = cv2.imread(dirname + "/" + imgs[0]).shape
            flag = 0
            for img in imgs:
                print(img)
                path = dirname + "/" + img
                id = img.split('.')[0]
                result = inference_detector(self.model, path)

                if isinstance(result, tuple):
                    bbox_result, segm_result = result
                else:
                    bbox_result, segm_result = result, None
                bboxes = np.vstack(bbox_result)
                scores = bboxes[:, -1]
                inds = scores > self.score
                bboxes = bboxes[inds, :]
                temp = []
                for bbox in bboxes:
                    bbox_int = bbox.astype(np.int32)
                    temp.append(bbox_int)
                newbbox = self.check_bbox(temp)
                filename = id + ".tif"
                xmlwriter = PascalVocWriter("VOC2007", filename, img_size)
                for box in newbbox:
                    xmlwriter.addBndBox(box[0], box[1], box[2], box[3], "nano", "0")
                xmlwriter.save(self.defaultSaveDir + "/" + id + ".xml")
                flag += 1
                if self.quick_flag == 1:
                    break
                prograssbar_value = round(flag / len(imgs), 2) * 100
                self.progressBarValue[int].emit(int(prograssbar_value))



    def check_bbox(self, all_bbox):
        new_bbox = []
        flag = []
        for i in range(len(all_bbox)):
            bbox = all_bbox[i]
            for j in range(len(all_bbox)):
                if i != j:
                    temp = all_bbox[j]
                    if abs(bbox[0] - temp[0]) <= 20 and abs(bbox[1] - temp[1]) <= 20:
                        if abs(bbox[2] - temp[2]) <= 20 and abs(bbox[3] - temp[3]) <= 20:
                            flag.append(i)
                            continue
        for i in range(len(all_bbox)):
            if i not in flag:
                new_bbox.append(all_bbox[i])
        return new_bbox

    def set_quick_flag(self, i):
        self.quick_flag = i





