import os
import math
import numpy as np
from  libs.read_bbox import read_bbox
import xml.dom.minidom
import cv2 as cv
from PyQt5.QtCore import *
from libs.pascal_voc_io import PascalVocWriter
class track(QThread):
    progressBarValue = pyqtSignal(int)
    after_track = pyqtSignal(int)
    def __init__(self, xml_dir, track_xml_dir, T=500, parent=None):
        super(track, self).__init__()
        self.SubImg_T = T

        self.xml_dir = xml_dir
        self.dir = os.listdir(self.xml_dir)
        self.dir = sorted(self.dir, key=lambda x: int(x.split(".")[0]))
        self.SubImg_Step = int(self.dir[1].split(".")[0]) - int(self.dir[0].split(".")[0])
        self.xml = [self.xml_dir + "/" + di for di in self.dir]

        self.track_xml_dir = track_xml_dir

        self.bboxs = [read_bbox.read(x) for x in self.xml]
        self.have_tracked = []  # 类似一个temp，主要将正在追踪的粒子放入，每帧都会对未放入新粒子的Particle进行计数，超过5则算跟踪结束
        self.quick_flag = 0

    def __del__(self):
        self.wait()

    def run(self):
        '''主循环，逐帧进行处理，每帧逐bbox进行处理，
           每个bbox：对self.have_tracked中的各个particle进行比较，求算质心距离，符合的则归为一类，不符合的则创建一类
           对一帧处理结束要给所有的正在追踪Particle + 1，而之前每次放入新的Particle轨迹会初始化其数值
        '''
        flag = 0
        for i in range(len(self.bboxs)):

            for j in range(len(self.bboxs[i])):
                bbox = self.bboxs[i][j]
                if len(bbox) == 5:
                    self.search(i, j, bbox)
            if len(self.have_tracked) > 0:
                for k in range(len(self.have_tracked)):
                    frame = int(self.dir[i].split(".")[0])

                    if self.have_tracked[k][0][2] != 'OVER':
                        if self.have_tracked[k][0][2] < 5:
                            self.have_tracked[k][0][2] += 1
                        # else:
                        #     self.have_tracked[k][0][2] = 'OVER'
                        elif (self.have_tracked[k][0][2] >= 5) and (frame % self.SubImg_T != 0):
                            self.have_tracked[k][0][2] = 'OVER'
            flag += 1
            if self.quick_flag == 1:
                break

            prograssbar_value = round(flag / len(self.bboxs), 2) * 100
            self.progressBarValue[int].emit(int(prograssbar_value))

        for i in range(len(self.bboxs)):
            newbbox = self.bboxs[i]
            name = int(self.dir[i].split(".")[0])
            filename = "%d.tif" % name
            xmlwriter = PascalVocWriter("VOC2007", filename, [523, 525, 1])
            for box in newbbox:
                xmlwriter.addBndBox(box[1], box[2], box[3], box[4], box[0], "0")
            xmlwriter.save(self.track_xml_dir + "/" + str(name) + ".xml")
        self.after_track[int].emit(1)


    def search(self, frame, box_id, bbox):
        '''TODO:现在用的是中心位置，后面可以换成图片最亮点的位置，这样精度会提高很多'''
        central = [(bbox[3] + bbox[1]) // 2, (bbox[4] + bbox[2]) // 2, 0]

        flag = -1  # 用来标志一个新的bbox是否被分入以前的类，如果没有则根据此flag重新创建一类
        if len(self.have_tracked) == 0:
            self.have_tracked.append([central, [int(self.dir[frame].split(".")[0]), box_id]])
            self.xml_modify(frame, box_id, 0)
        else:
            for i in range(len(self.have_tracked)):
               # print(i, self.have_tracked)
                if self.have_tracked[i][0][2] != 'OVER':
                    temp = self.have_tracked[i][0]
                    dist = self.distEclud(central, temp)

                    if dist < 30:
                        flag = 1

                        self.have_tracked[i].append([int(self.dir[frame].split(".")[0]), box_id])

                        self.update_mass_central(i)
                        self.xml_modify(frame, box_id, i)
                        break

            if flag == -1:
               # print(frame, 'dist too long')
                self.have_tracked.append([central, [int(self.dir[frame].split(".")[0]), box_id]])
                self.xml_modify(frame, box_id, len(self.have_tracked) - 1)

    def update_mass_central(self, ID):
        '''更新质心位置，每次放入新的粒子都需要更新'''
        ID_info = self.have_tracked[ID]
        x = 0
        y = 0

        for i in range(len(ID_info) - 1):
            frame_name = ID_info[i + 1][0]
            temp_box_id = ID_info[i + 1][1]

            # bboxs = read_bbox.read(self.xml_dir + "/" + str(frame_name) + ".xml")
            # print(frame_name, temp_box_id)
            # frame name 一般从1开始，
            bboxs = self.bboxs[(frame_name - 1) // self.SubImg_Step][temp_box_id]
            temp_x, temp_y = self.get_central_point(bboxs)
            x += temp_x
            y += temp_y

        x_mean = x // (len(ID_info) - 1)
        y_mean = y // (len(ID_info) - 1)
        self.have_tracked[ID][0][0:3] = [x_mean, y_mean, 0]

    def get_central_point(self, bbox):
        return (bbox[3]+bbox[1]) // 2, (bbox[4]+bbox[2]) // 2
    def distEclud(self, vecA, vecB):
        """欧式距离
        输入：向量A, 向量B
        输出：两个向量的欧式距离
        """
        a = (vecA[0] - vecB[0]) ** 2
        b = (vecA[1] - vecB[1]) ** 2
        return math.sqrt(a + b)

    def xml_modify(self, frame, box_id, ID, find_debinding=0):
        '''用于修改每个Particle的分类'''
        name = self.bboxs[frame][box_id][0]
        if name in ["NONE", "None", "none"]:
            self.bboxs[frame][box_id][0] = "NONE" + "__ID:" + str(ID)
            for i in range(1, len(self.have_tracked[ID])):
                if [int(self.dir[frame].split(".")[0]), box_id] == self.have_tracked[ID][i]:
                    self.have_tracked[ID][i].append("NONE" + "__ID:" + str(ID))
                    self.have_tracked[ID][0].append("Have None")

        elif len(self.have_tracked[ID][0]) == 4:
            self.bboxs[frame][box_id][0] = "NONE" + "__ID:" + str(ID)
        else:
            self.bboxs[frame][box_id][0] = "__ID:" + str(ID)


    def over_tracked(self):
        return self.have_tracked, self.bboxs

    def set_quick_flag(self, i):
        self.quick_flag = i


