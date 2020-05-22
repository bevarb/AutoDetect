import os
import math
from xml import sax
import xml.dom.minidom
class Box_Handler(sax.ContentHandler):  # 定义自己的handler类，继承sax.ContentHandler
    def __init__(self):
        sax.ContentHandler.__init__(self)  # 弗父类和子类都需要初始化（做一些变量的赋值操作等）
        self.CurrentData = ""
        self.tag = ""
        self.xmin = ""
        self.ymin = ""
        self.xmax = ""
        self.ymax = ""
        self.temp = []
        self.box = []



    def startElement(self, name, attrs):  # 遇到<tag>标签时候会执行的方法，这里的name，attrs不用自己传值的（这里其实是重写）
        self.CurrentData = name

    def endElement(self, name):
    # 遇到</tag>执行的方法，name不用自己传值（重写）
    # print "endElement"
        if name == "name":
            self.temp.append(self.tag)
        elif name == "xmin":
            self.temp.append(int(self.xmin))
        elif name == "ymin":
            self.temp.append(int(self.ymin))
        elif name == "xmax":
            self.temp.append(int(self.xmax))
        elif name == "ymax":
            self.temp.append(int(self.ymax))
        elif name == "object":
            self.box.append(self.temp)
            self.temp = []
        elif name == "annotation":
            global Box
            Box = self.box
        self.CurrentData = ""
        return self.box
    def characters(self, content):  # 获取标签内容
        if self.CurrentData == "name":
            self.tag = content
        elif self.CurrentData == "xmin":
            self.xmin = content
        elif self.CurrentData == "ymin":
            self.ymin = content
        elif self.CurrentData == "xmax":
            self.xmax = content
        elif self.CurrentData == "ymax":
            self.ymax = content

def read_box(path):
    '''读取xml文件，并返回box的列表[[name,xmin,ymin,xmax,ymax], [name,xmin,ymin,xmax,ymax]]'''
    parser = sax.make_parser()  # 创建一个 XMLReader
    parser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
    Handler = Box_Handler()  # 重写 ContextHandler
    parser.setContentHandler(Handler)
    parser.parse(path)
    return Box

from PyQt5.QtCore import *
class track(QThread):
    progressBarValue = pyqtSignal(int)
    def __init__(self, xml_dir, parent=None):
        super(track, self).__init__()
        dir = os.listdir(xml_dir)
        dir = sorted(dir, key=lambda x: int(x.split(".")[0]))
        self.xml = [xml_dir + "/" + di for di in dir]
        self.bboxs = [read_box(x) for x in self.xml]
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
                for i in range(len(self.have_tracked)):

                    if self.have_tracked[i][0][2] != 'OVER':
                        if self.have_tracked[i][0][2] < 5:
                            self.have_tracked[i][0][2] += 1
                        else:
                            self.have_tracked[i][0][2] = 'OVER'
            flag += 1
            if self.quick_flag == 1:
                break
            prograssbar_value = round(flag / len(self.bboxs), 2) * 100
            self.progressBarValue.emit(prograssbar_value)


    def search(self, frame, box_id, bbox):
        '''TODO:现在用的是中心位置，后面可以换成图片最亮点的位置，这样精度会提高很多'''
        central = [(bbox[3] + bbox[1]) // 2, (bbox[4] + bbox[2]) // 2, 0]
        flag = -1  # 用来标志一个新的bbox是否被分入以前的类，如果没有则根据此flag重新创建一类
        if len(self.have_tracked) == 0:
            self.have_tracked.append([central, [frame, box_id]])
            self.xml_modify(frame, box_id, 0)
        else:
            for i in range(len(self.have_tracked)):
               # print(i, self.have_tracked)
                if self.have_tracked[i][0][2] != 'OVER':
                    temp = self.have_tracked[i][0]
                    dist = self.distEclud(central, temp)
                    # print(central, temp, dist)
                    if dist < 30:
                        flag = 1
                        self.have_tracked[i].append([frame, box_id])
                        # print(i, '--', self.have_tracked)
                        self.update_mass_central(i)
                        self.xml_modify(frame, box_id, i)
                        break
            if flag == -1:
               # print(frame, 'dist too long')
                self.have_tracked.append([central, [frame, box_id]])
                self.xml_modify(frame, box_id, len(self.have_tracked) - 1)

    def update_mass_central(self, ID):
        '''更新质心位置，每次放入新的粒子都需要更新'''
        ID_info = self.have_tracked[ID]
        x = 0
        y = 0
        for i in range(len(ID_info) - 1):
            temp_frame = ID_info[i + 1][0]
            temp_box_id = ID_info[i + 1][1]
            temp_x, temp_y = self.get_central_point(self.bboxs[temp_frame][temp_box_id])
            x += temp_x
            y += temp_y
        x_mean = x // (len(ID_info) - 1)
        y_mean = y // (len(ID_info) - 1)
        self.have_tracked[ID][0] = [x_mean, y_mean, 0]

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

    def xml_modify(self, frame, box_id, ID):
        '''用于修改每个Particle的分类'''
        xml_path = self.xml[frame]
        type = self.bboxs[frame][box_id][0]
        dom = xml.dom.minidom.parse(xml_path)
        root = dom.documentElement
        name = root.getElementsByTagName('name')
        name[box_id].firstChild.data = type + "__ID:" + str(ID)
        print('Frame %d , box_id %d have been modified %s %d' % (frame, box_id, type, ID))
        # print(self.bboxs[frame][box_id])
        with open(xml_path, 'w') as fh:
            dom.writexml(fh)

    def over_tracked(self):
        return self.have_tracked

    def set_quick_flag(self, i):
        self.quick_flag = i


