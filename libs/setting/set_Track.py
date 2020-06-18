from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_Track(QDialog):
    set_SubImg_sig = pyqtSignal(int)
    def __init__(self, method=0, parent=None):
        super(set_Track, self).__init__()
        self.method = method

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
        layout1.addWidget(lable1)
        layout1.addWidget(self.cob1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)


        layout7 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout7.addWidget(ok_btn)
        layout7.addWidget(cancle_btn)
        Wid7 = QWidget()
        Wid7.setLayout(layout7)

        layout.addWidget(Wid1)
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
            self.set_SubImg_sig.emit(method)
            self.dialog.close()

        cancle_btn.clicked.connect(_cancle)
        ok_btn.clicked.connect(_ok)






