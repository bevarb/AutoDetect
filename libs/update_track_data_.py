import os
from  libs.read_bbox import read_bbox
from PyQt5.QtCore import *

class update_track_data(QThread):
    progressBarValue = pyqtSignal(int)
    after_track = pyqtSignal(int)
    def __init__(self, track_xml_dir, parent=None):
        super(update_track_data, self).__init__()

        self.xml_dir = track_xml_dir
        self.dir = os.listdir(self.xml_dir)
        self.dir = sorted(self.dir, key=lambda x: int(x.split(".")[0]))
        self.xml = [self.xml_dir + "/" + di for di in self.dir]

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
        for i in range(len(self.bboxs)):
            if len(self.bboxs[i]) != 0:
                for j in range(len(self.bboxs[i])):
                    name = self.bboxs[i][j][0]
                    ID = int(name.split("ID:")[-1].split("|")[0])
                    Frame = int(self.dir[i].split(".")[0])
                    type = self.bboxs[i][j][0].split("|")[1]
                    central = self.get_central(self.bboxs[i][j])
                    intensity = self.bboxs[i][j][5]
                    # 如果ID较大，但是have_tracked内的数组没有这么多，则新建多个
                    if len(self.have_tracked) < ID + 1:
                        new_list_num = ID - len(self.have_tracked) + 1
                        for k in range(new_list_num):
                            self.have_tracked.append([[0, 0, 0]])
                    # 下面是名字中含有NONE，这是之前的，先保留
                    if ("NONE" in name) and (len(self.have_tracked[ID][0]) == 3):
                        self.have_tracked[ID][0].append("Have None")
                        self.have_tracked[ID].append([Frame, j, "NONE__ID:%d" % ID])
                    # 正常的颗粒进行处理，按照ID放入，更新中心距离
                    self.have_tracked[ID][0][0:2] = central
                    self.have_tracked[ID].append([Frame, j, type, intensity])

        self.after_track[int].emit(2)


    def over_tracked(self):
        return self.have_tracked, self.bboxs

    def get_central(self, bbox):
        return (bbox[3]+bbox[1]) // 2, (bbox[4]+bbox[2]) // 2



