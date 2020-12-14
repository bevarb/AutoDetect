from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_Merge(QDialog):
    set_Merge_sig = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(set_Merge, self).__init__()

    def show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("选择需要合并的两类")
        self.dialog.resize(350, 100)
        layout = QVBoxLayout()

        layout2 = QHBoxLayout()
        lable21 = QLabel("Class1：")
        self.LineEdit21 = QLineEdit()
        lable22 = QLabel("Class2：")
        self.LineEdit22 = QLineEdit()
        layout2.addWidget(lable21)
        layout2.addWidget(self.LineEdit21)
        layout2.addWidget(lable22)
        layout2.addWidget(self.LineEdit22)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)


        layout7 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout7.addWidget(ok_btn)
        layout7.addWidget(cancle_btn)
        Wid7 = QWidget()
        Wid7.setLayout(layout7)

        layout.addWidget(Wid2)
        layout.addWidget(Wid7)
        self.dialog.setLayout(layout)
        self.dialog.show()

        def _cancle():
            self.dialog.close()
        def _ok():
            self.dialog.close()
            self.set_Merge_sig.emit(int(self.LineEdit21.text()),
                                     int(self.LineEdit22.text()))

        cancle_btn.clicked.connect(_cancle)
        ok_btn.clicked.connect(_ok)

