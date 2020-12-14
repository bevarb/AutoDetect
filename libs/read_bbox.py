from xml import sax

class Box_Handler(sax.ContentHandler):  # 定义自己的handler类，继承sax.ContentHandler
    def __init__(self):
        sax.ContentHandler.__init__(self)  # 弗父类和子类都需要初始化（做一些变量的赋值操作等）
        self.CurrentData = ""
        self.tag = ""
        self.xmin = ""
        self.ymin = ""
        self.xmax = ""
        self.ymax = ""
        self.intensity = ""
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
        elif name == "intensity":
            self.temp.append(float(self.intensity))
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
        elif self.CurrentData == "intensity":
            self.intensity = content

class read_bbox():

    def read(path):
        '''读取xml文件，并返回box的列表[[name,xmin,ymin,xmax,ymax, intensity], [name,xmin,ymin,xmax,ymax, intensity]]'''
        parser = sax.make_parser()  # 创建一个 XMLReader
        parser.setFeature(sax.handler.feature_namespaces, 0)  # turn off namepsaces
        Handler = Box_Handler()  # 重写 ContextHandler
        parser.setContentHandler(Handler)
        parser.parse(path)
        return Box