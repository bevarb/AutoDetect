import os
import math
import numpy as np
from libs.read_bbox import read_bbox
import xml.dom.minidom
import cv2 as cv
from PyQt5.QtCore import *
from libs.pascal_voc_io import PascalVocWriter
class track(QThread):
    progressBarValue = pyqtSignal(int)
    after_track = pyqtSignal(int)
    def __init__(self, xml_dir, track_xml_dir, L_limit=20, Frame_limit=5, Method=0, T=500, parent=None):
        super(track, self).__init__()
        self.SubImg_T = T  # 减背景的间隔
        self.Method = Method  # 跟踪的方法
        self.L_limit = L_limit  # 前后两帧相同particle之间的中心距离
        self.Frame_limit = Frame_limit  # 同一个particle多长时间没有更新的限制

        self.xml_dir = xml_dir
        self.dir = os.listdir(self.xml_dir)
        self.dir = sorted(self.dir, key=lambda x: int(x.split(".")[0]))
        self.SubImg_Step = int(self.dir[1].split(".")[0]) - int(self.dir[0].split(".")[0])
        self.xml = [self.xml_dir + "/" + di for di in self.dir]  # 检测后的标记文件

        self.track_xml_dir = track_xml_dir  # 跟踪后的标记文件

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
        for i in range(len(self.bboxs)):  # 每一个图片

            for j in range(len(self.bboxs[i])):  # 判断
                bbox = self.bboxs[i][j]
                if len(bbox) == 6:  # 框的参数必须为5
                    self.search(i, j, bbox)
            if len(self.have_tracked) > 0:
                # TODO：这里后面需要修改，将两种方法合并为一种
                win_no_nano = self.Frame_limit
                if self.Method == 0:  # 减第一帧所用的track
                    for k in range(len(self.have_tracked)):  # 对已经跟踪的类进行比较
                        if self.have_tracked[k][0][2] != 'OVER':
                            if self.have_tracked[k][0][2] < win_no_nano:
                                self.have_tracked[k][0][2] += 1
                            # else:
                            #     self.have_tracked[k][0][2] = 'OVER'
                            elif (self.have_tracked[k][0][2] >= win_no_nano) and (self.have_tracked[k][-1][0] % self.SubImg_T != 0):
                                self.have_tracked[k][0][2] = 'OVER'
                elif self.Method == 1:  # 减前一帧所用的track
                    for k in range(len(self.have_tracked)):
                        if self.have_tracked[k][0][2] != 'OVER':
                            if self.have_tracked[k][0][2] < win_no_nano:
                                self.have_tracked[k][0][2] += 1
                            if len(self.have_tracked[k]) >= 2 and self.have_tracked[k][0][2] >= 5:  # 里面只有第一帧和最后一帧
                                if self.have_tracked[k][-1][2] == "debinding":
                                    self.have_tracked[k][0][2] = 'OVER'
            # 进度条的加载
            flag += 1
            if self.quick_flag == 1:
                break
            prograssbar_value = round(flag / len(self.bboxs), 2) * 100
            self.progressBarValue[int].emit(int(prograssbar_value))

        # 将跟踪后的写入
        for i in range(len(self.bboxs)):
            newbbox = self.bboxs[i]
            name = int(self.dir[i].split(".")[0])
            filename = "%d.tif" % name
            xmlwriter = PascalVocWriter("VOC2007", filename, [523, 525, 1])
            for box in newbbox:
                xmlwriter.addBndBox(box[1], box[2], box[3], box[4], box[0], "0", box[5])
            xmlwriter.save(self.track_xml_dir + "/" + str(name) + ".xml")
        self.after_track[int].emit(1)


    def search(self, frame, box_id, bbox):
        '''TODO:现在用的是中心位置，后面可以换成图片最亮点的位置，这样精度会提高很多'''
        central = [(bbox[3] + bbox[1]) // 2, (bbox[4] + bbox[2]) // 2, 0]

        flag = -1  # 用来标志一个新的bbox是否被分入以前的类，如果没有则根据此flag重新创建一类
        if len(self.have_tracked) == 0:  # 当have_tracked里面没有内容时新建第一个
            self.have_tracked.append([central, [int(self.dir[frame].split(".")[0]), box_id, bbox[0], bbox[5]]])
            self.xml_modify(frame, box_id, 0)
        else:
            for i in range(len(self.have_tracked)):  # 当have_tracked里面有内容时进行寻找，寻找到则将flag设置为1，并添加到have_tracked
                                                     # 更新中心位置，修改对应的Box名称
                if self.have_tracked[i][0][2] != 'OVER':
                    temp = self.have_tracked[i][0]
                    dist = self.distEclud(central, temp)
                    if dist < self.L_limit:
                        name = self.bboxs[frame][box_id][0]
                        if (self.have_tracked[i][-1][0] % self.SubImg_T == 0) \
                                                and (name not in ["NONE", "None", "none"])\
                                            and self.Method == 0:
                            pass   # 如果跟踪到了刷新帧，而且名字也不包含none，那么就break重新创建
                        else:
                            flag = 1  # 如果不在刷新帧，或者在刷新帧但是名字包含none，那么就归为一类

                            self.have_tracked[i].append([int(self.dir[frame].split(".")[0]), box_id, bbox[0], bbox[5]])

                            self.update_mass_central(i)
                            self.xml_modify(frame, box_id, i)
                            break
            # # 先遍历一遍，得到最短距离，其最短距离的ID
            # min_info = []
            # for i in range(len(self.have_tracked)):  # 当have_tracked里面有内容时进行寻找，寻找到则将flag设置为1，并添加到have_tracked
            #                                          # 更新中心位置，修改对应的Box名称
            #    # print(i, self.have_tracked)
            #     if self.have_tracked[i][0][2] != 'OVER':
            #         temp = self.have_tracked[i][0]
            #         dist = self.distEclud(central, temp)
            #         min_info.append([dist, i])
            # min_info = sorted(min_info, key=lambda x: x[0])
            # # 按照排序后的距离进行循环，看是否有能够满足条件的
            # for min_L, min_ID in min_info:
            #     if min_L < self.L_limit:
            #         name = self.bboxs[frame][box_id][0]
            #         # 这个if的用法是，在刷新帧的位置有一些Particle，然后后面又出现了新的比较像的颗粒，那是应该重新创建的，而不是归为一类
            #         if (self.have_tracked[min_ID][-1][0] % self.SubImg_T == 0) \
            #                 and (name not in ["NONE", "None", "none"])\
            #                 and self.Method == 0:
            #             pass
            #         elif frame == self.have_tracked[min_ID][-1][0]:
            #             # 如果当前的Frame与跟踪的这个ID最后的Frame一样，那也要跳过，毕竟同一帧不能出现两个ID
            #             pass
            #         else:
            #             flag = 1  # 如果不在刷新帧，或者在刷新帧但是名字包含none，那么就归为一类
            #             self.have_tracked[min_ID].append([int(self.dir[frame].split(".")[0]), box_id, bbox[0]])
            #             # self.update_mass_central(i)
            #             self.have_tracked[min_ID][0][0:3] = central
            #             self.xml_modify(frame, box_id, min_ID)
            #             break
            #     else:
            #         break

            if flag == -1:  # flag == -1说明have_tracked里面没有能归为一类的类，这时自创一类
               # print(frame, 'dist too long')
                self.have_tracked.append([central, [int(self.dir[frame].split(".")[0]), box_id, bbox[0], bbox[5]]])
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
            self.bboxs[frame][box_id][0] = "ID:" + str(ID) + "|%s" % name + "|%s" % self.bboxs[frame][box_id][5]


    def over_tracked(self):
        return self.have_tracked, self.bboxs

    def set_quick_flag(self, i):
        self.quick_flag = i