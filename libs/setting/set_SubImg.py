from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_SubImg(QThread):
    set_SubImg_sig = pyqtSignal(int, int, int)
    def __init__(self, method=0, T=500, Step=1, parent=None):
        super(set_SubImg, self).__init__()
        self.method = method
        self.T = T
        self.Step = Step
    def __del__(self):
        self.wait()

    def run(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("设置处理格式")
        self.dialog.resize(350, 200)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel("处理格式:")
        self.cob1 = QComboBox()
        self.cob1.addItem("减第一帧")
        self.cob1.addItem("逐帧相减")
        self.cob1.setCurrentIndex(self.method)
        self.cob1.currentIndexChanged.connect(self.cob_change)
        layout1.addWidget(lable1)
        layout1.addWidget(self.cob1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        lable2 = QLabel("刷新周期：")
        self.lineedit2 = QLineEdit(str(self.T))
        layout2.addWidget(lable2)
        layout2.addWidget(self.lineedit2)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)

        layout3 = QHBoxLayout()
        lable3 = QLabel("步长：")
        self.lineedit3 = QLineEdit(str(self.Step))
        layout3.addWidget(lable3)
        layout3.addWidget(self.lineedit3)
        Wid3 = QWidget()
        Wid3.setLayout(layout3)

        layout4 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout4.addWidget(ok_btn)
        layout4.addWidget(cancle_btn)
        Wid4 = QWidget()
        Wid4.setLayout(layout4)

        layout.addWidget(Wid1)
        layout.addWidget(Wid2)
        layout.addWidget(Wid3)
        layout.addWidget(Wid4)
        self.dialog.setLayout(layout)
        self.dialog.show()
        ok_btn.clicked.connect(self.dialog.close)

        def _cancle():
            self.lineedit2.clear()
            self.dialog.close()
        cancle_btn.clicked.connect(_cancle)
        ret = self.dialog.exec_()

        if ret == 0:
            method = -1
            if self.cob1.currentIndex() == 0:
                method = 0
            else:
                method = 1
            if len(self.lineedit2.text()) != 0:
                self.set_SubImg_sig.emit(method, int(self.lineedit2.text()), int(self.lineedit3.text()))

    def cob_change(self, text):
        if text == 1:
            self.lineedit2.setText("None")
    # def set_value(self, i):
    #     self.progressBar.setValue(i)
    #     if i == 100:
    #         self.dialog.close()