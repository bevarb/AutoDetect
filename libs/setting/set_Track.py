from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_Track(QDialog):
    set_SubImg_sig = pyqtSignal(int, int, int, int)
    def __init__(self, method=0, T=100, parent=None):
        super(set_Track, self).__init__()
        self.method = method
        self.T = T

    def show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("选择跟踪方式")
        self.dialog.resize(350, 100)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel("处理格式:")
        self.cob1 = QComboBox()
        self.cob1.addItem("减第一帧(Track1)")
        self.cob1.addItem("逐帧相减(Track2)")
        self.cob1.setCurrentIndex(self.method)
        self.cob1.currentIndexChanged.connect(self.cob_change)
        layout1.addWidget(lable1)
        layout1.addWidget(self.cob1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        lable21 = QLabel("距离限制：")
        self.LineEdit21 = QLineEdit("20")
        lable22 = QLabel("最长空帧数：")
        self.LineEdit22 = QLineEdit("5")
        lable23 = QLabel("周期T：")
        self.LineEdit23 = QLineEdit(str(self.T))
        layout2.addWidget(lable21)
        layout2.addWidget(self.LineEdit21)
        layout2.addWidget(lable22)
        layout2.addWidget(self.LineEdit22)
        layout2.addWidget(lable23)
        layout2.addWidget(self.LineEdit23)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)


        layout7 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout7.addWidget(ok_btn)
        layout7.addWidget(cancle_btn)
        Wid7 = QWidget()
        Wid7.setLayout(layout7)

        layout.addWidget(Wid1)
        layout.addWidget(Wid2)
        layout.addWidget(Wid7)
        self.dialog.setLayout(layout)
        self.dialog.show()

        def _cancle():
            self.dialog.close()
        def _ok():
            method = -1
            if self.cob1.currentIndex() == 0:
                method = 0
            else:
                method = 1
            self.dialog.close()
            self.set_SubImg_sig.emit(method,
                                     int(self.LineEdit21.text()),
                                     int(self.LineEdit22.text()),
                                     int(self.LineEdit23.text()))


        cancle_btn.clicked.connect(_cancle)
        ok_btn.clicked.connect(_ok)

    def cob_change(self, text):
        if text == 1:
            self.LineEdit23.setText("1")
            self.LineEdit22.setText("5")






