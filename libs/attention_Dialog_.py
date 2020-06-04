from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class Attention(QDialog):
    open_updateTrack_Sig = pyqtSignal(str)
    def __init__(self, text, flag=0, parent=None):
        super(Attention, self).__init__()
        self.text = text
        self.flag = flag  # flag=0 is to attention user to update track data
                          # flag=1 is to attention some others


    def Show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Attention")
        self.dialog.resize(350, 200)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel(self.text)
        lable1.adjustSize()
        lable1.setWordWrap(True)
        lable1.setAlignment(Qt.AlignJustify)
        layout1.addWidget(lable1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        ok_btn = QPushButton("ok")
        cancle_btn = QPushButton("cancel")
        layout2.addWidget(ok_btn)
        layout2.addWidget(cancle_btn)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)

        layout.addWidget(Wid1)
        layout.addWidget(Wid2)

        self.dialog.setLayout(layout)
        self.dialog.show()
        ok_btn.clicked.connect(self.send_ok)

        def _cancle():
            self.dialog.close()
        cancle_btn.clicked.connect(_cancle)



    def send_ok(self):
        if self.flag == 0:
            self.open_updateTrack_Sig[str].emit("Open Update Track Data")

        self.dialog.close()



