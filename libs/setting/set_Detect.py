from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_Detect(QDialog):
    set_Detect_sig = pyqtSignal(int, float)
    def __init__(self, parent=None):
        super(set_Detect, self).__init__()

    def show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("选择加载模型")
        self.dialog.resize(350, 100)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel("模型:")
        self.cob1 = QComboBox()
        self.cob1.addItem("Model1")
        self.cob1.addItem("Model2")
        self.cob1.setCurrentIndex(0)
        layout1.addWidget(lable1)
        layout1.addWidget(self.cob1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        lable2 = QLabel("阈值:")
        self.lineedit2 = QLineEdit("0.5")

        layout2.addWidget(lable2)
        layout2.addWidget(self.lineedit2)
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
            method = self.cob1.currentIndex()
            self.dialog.close()
            self.set_Detect_sig.emit(method, float(self.lineedit2.text()))


        cancle_btn.clicked.connect(_cancle)
        ok_btn.clicked.connect(_ok)






