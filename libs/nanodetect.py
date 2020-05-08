from mmdet.apis import init_detector, inference_detector, show_result
import numpy as np
import os
import cv2
# 首先下载模型文件https://s3.ap-northeast-2.amazonaws.com/open-mmlab/mmdetection/models/faster_rcnn_r50_fpn_1x_20181010-3d1b3351.pth
class detect():
    def __init__(self, model_name):
        config_file = 'libs/detect/configs/RetinaNet.py'
        checkpoint_file = model_name
        # 初始化模型
        self.model = init_detector(config_file, checkpoint_file)
    def dir(self, dirname):
        # 测试一张图片
        imgs = os.listdir(dirname)
        all_bbox = []
        all_id = []
        img_size = []
        if imgs is not None:
            imgs = sorted(imgs, key=lambda x: int(x.split('/')[-1].split('.')[0]))
            img_size = cv2.imread(dirname + "/" + imgs[0]).shape
            for img in imgs:
                print(img)
                path = dirname + "/" + img
                id = img.split('.')[0]
                all_id.append(id)
                result = inference_detector(self.model, path)

                if isinstance(result, tuple):
                    bbox_result, segm_result = result
                else:
                    bbox_result, segm_result = result, None
                bboxes = np.vstack(bbox_result)
                scores = bboxes[:, -1]
                inds = scores > 0.3
                bboxes = bboxes[inds, :]
                temp = []
                for bbox in bboxes:
                    bbox_int = bbox.astype(np.int32)
                    temp.append(bbox_int)
                    # left_top = (bbox_int[0], bbox_int[1])
                    # right_bottom = (bbox_int[2], bbox_int[3])
                all_bbox.append(temp)

        return all_bbox, all_id, img_size

