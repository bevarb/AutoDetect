from xml import sax
import os
import cv2
from shutil import copyfile
class Box_Handler(sax.ContentHandler):  # 定义自己的handler类，继承sax.ContentHandler
    def __init__(self):
        sax.ContentHandler.__init__(self)  # 父类和子类都需要初始化（做一些变量的赋值操作等）
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
        if name == "xmin":
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
    '''读取xml文件，并返回box的列表[[xmin,ymin,xmax,ymax], [xmin,ymin,xmax,ymax]]'''
    parser = sax.make_parser()  # 创建一个 XMLReader
    parser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
    Handler = Box_Handler()  # 重写 ContextHandler
    parser.setContentHandler(Handler)
    parser.parse(path)
    return Box
all_xml = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/All_Annotations"
source_xml = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/binding_Annotations"
source_tifs = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/binding_tifs"
target_xml = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/debinding_Annotations"
target_tifs = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/debinding_tifs"
di = os.listdir(source_tifs)
di = sorted(di, key=lambda x: int(x.split(".")[0]))
path = [source_tifs + "/" + d for d in di]
j = 0
for i in range(len(path)):
    # box = read_box(path[i])
    # if len(box) == 0:
    #     copyfile(all_xml + ("/%d" % i) + ".xml", target_xml + ("/%d" % i) + ".xml")
    img = cv2.imread(source_tifs + ("/%d" % i) + ".tif")
    img = cv2.bitwise_not(img)
    cv2.imwrite(target_tifs + ("/%d" % i) + ".tif", img)
        # j += 1

print('There have %d xmls dont have bbox' % j)