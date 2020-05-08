from xml import sax
import os
import cv2
import pandas as pd
import numpy as np
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

def get_undo_list(path, flag):
    '''获取目标路径中的所有文件，并按顺序排好，返回未处理文件路径的列表'''
    all_xml = os.listdir(path)
    #all_xml = sorted(all_xml, key=lambda x: int(x.split('.')[-2]))
    print(all_xml)
    undo_xml = []
    for i in range(len(all_xml)):
        name = all_xml[i].split('.')[-2]

        if flag in name:
            pass
        else:
            undo_xml.append(path + "\\" + all_xml[i])
    undo_xml = sorted(undo_xml, key=lambda x: int(x.split('.')[-2].split('\\')[-1][0]))
    return undo_xml

def pasete_img(soure_path, target_file, flag):
    '''读取图片中的所有box并保存'''
    img = cv2.imread(soure_path)
    target_path = target_file + "/" + str(flag) + '.tif'
    if not os.path.exists(target_path):
        cv2.imwrite(target_path, img)
    flag += 1
    return target_path, flag

if __name__ == "__main__":
    # 1-循环读取所有文件夹-按顺序
    # 2-循环读取所有xml文件-按顺序
    # 3-读取所有Box
    # 4-将Box全部放入一个excel文件
    # 5-将图片全部放入一个文件夹

    Source_root = "D:\Project_Data\First\clear_data"
    Target_file = "D:/Project_Data/First/Detect_data/img"
    flag = 0
    Boxs = []
    for k in range(0, 15):
        pa = 'class_%d' % (k)
        Source_file = Source_root + '\class_' + str(k) + '_xml'
        Img_file = Source_root + '\class_' + str(k)
        if not os.path.exists(Target_file):
            os.makedirs(Target_file, exist_ok=True)
        # if pa == 'test_1':
        #     continue
        flag = len(os.listdir(Target_file))   # 这个flag用来记录目标文件夹中的图片数量，从而按顺序命名
        undo_xml = get_undo_list(Source_file, 'dd')

        for i in range(len(undo_xml)):
             Img_path = Img_file + "\\" + undo_xml[i].split(".")[-2].split("\\")[-1][0] + ".tif"
             target_path, flag = pasete_img(Img_path, Target_file, flag)
             Box = read_box(undo_xml[i])
             Box.insert(0, target_path)
             Boxs.append(Box)
    df = pd.DataFrame(Boxs)
    # df = df.T
    print(df)
    writer = pd.ExcelWriter('test.xlsx')  # 写入Excel文件
    df.to_excel(writer, 'page_1', float_format='%.2f')
    writer.save()
    writer.close()







