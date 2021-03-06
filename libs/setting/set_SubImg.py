from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_SubImg(QDialog):
    set_SubImg_sig = pyqtSignal(int, int, int, int, float, str, str, int, int, int)
    def __init__(self, method=0, T=500, Step=1, Flag="_", Flag_Num="-1", parent=None):
        super(set_SubImg, self).__init__()
        self.method = method
        self.T = T
        self.Step = Step
        self.Flag = Flag
        self.Flag_Num = Flag_Num


    def show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("设置处理格式")
        self.dialog.resize(350, 400)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1_1 = QLabel("处理格式:")
        self.cob1 = QComboBox()
        self.cob1.addItem("减第一帧")
        self.cob1.addItem("逐帧相减")
        self.cob1.setCurrentIndex(self.method)
        self.cob1.currentIndexChanged.connect(self.cob_change)
        self.checkbox1 = QCheckBox("Mean")
        self.checkbox1.setChecked(False)
        self.checkbox2 = QCheckBox("32Bit")
        self.checkbox2.setChecked(True)
        self.checkbox3 = QCheckBox("Reverse")
        self.checkbox3.setChecked(False)

        layout1.addWidget(lable1_1)
        layout1.addWidget(self.cob1)
        layout1.addWidget(self.checkbox1)
        layout1.addWidget(self.checkbox2)
        layout1.addWidget(self.checkbox3)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        lable21 = QLabel("Sub T：")
        self.lineedit21 = QLineEdit(str(self.T))
        lable22 = QLabel("Step：")
        self.lineedit22 = QLineEdit(str(self.Step))
        lable23 = QLabel("Mean Step：")
        self.lineedit23 = QLineEdit(str(self.Step))
        lable24 = QLabel("Gamma：")
        self.lineedit24 = QLineEdit(str(0.4))
        layout2.addWidget(lable21)
        layout2.addWidget(self.lineedit21)
        layout2.addWidget(lable22)
        layout2.addWidget(self.lineedit22)
        layout2.addWidget(lable23)
        layout2.addWidget(self.lineedit23)
        layout2.addWidget(lable24)
        layout2.addWidget(self.lineedit24)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)

        layout3 = QHBoxLayout()
        lable3 = QLabel("选择原始图片的一个范例")
        choose_btn = QPushButton("选择")
        layout3.addWidget(lable3)
        layout3.addWidget(choose_btn)
        Wid3 = QWidget()
        Wid3.setLayout(layout3)

        layout4 = QHBoxLayout()
        self.lable4 = QLabel("None")
        layout4.addWidget(self.lable4)
        Wid4 = QWidget()
        Wid4.setLayout(layout4)

        layout5 = QHBoxLayout()
        lable5 = QLabel("标志符：")
        self.lineedit4 = QLineEdit("_")
        lable6 = QLabel("顺序(0/1/2)：")
        self.lineedit5 = QLineEdit("1")
        update_btn = QPushButton("Update")
        layout5.addWidget(lable5)
        layout5.addWidget(self.lineedit4)
        layout5.addWidget(lable6)
        layout5.addWidget(self.lineedit5)
        layout5.addWidget(update_btn)
        Wid5 = QWidget()
        Wid5.setLayout(layout5)

        layout6 = QHBoxLayout()
        self.lable7 = QLabel("None")
        layout6.addWidget(self.lable7)
        Wid6 = QWidget()
        Wid6.setLayout(layout6)

        layout7 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout7.addWidget(ok_btn)
        layout7.addWidget(cancle_btn)
        Wid7 = QWidget()
        Wid7.setLayout(layout7)

        layout.addWidget(Wid1)
        layout.addWidget(Wid2)
        layout.addWidget(Wid3)
        layout.addWidget(Wid4)
        layout.addWidget(Wid5)
        layout.addWidget(Wid6)
        layout.addWidget(Wid7)
        self.dialog.setLayout(layout)
        self.dialog.show()
        ok_btn.clicked.connect(self.dialog.close)
        choose_btn.clicked.connect(self.get_filename)
        update_btn.clicked.connect(self.get_list)

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
            if len(self.lineedit22.text()) != 0:
                is_mean = 1 if self.checkbox1.isChecked() else 0
                is_32Bit = 1 if self.checkbox2.isChecked() else 0
                is_reverse = 1 if self.checkbox3.isChecked() else 0
                self.set_SubImg_sig.emit(method,
                                         int(self.lineedit21.text()),
                                         int(self.lineedit22.text()),
                                         int(self.lineedit23.text()),
                                         float(self.lineedit24.text()),
                                         self.lineedit4.text(),
                                         self.lineedit5.text(),
                                         is_mean,
                                         is_32Bit,
                                         is_reverse)

    def cob_change(self, text):
        if text == 1:
            self.lineedit21.setText("1")
            self.lineedit22.setText("5")
            self.lineedit23.setText("5")
            self.checkbox1.setChecked(True)


    def get_filename(self):
        filename, filetype = QFileDialog.getOpenFileName(None, "选取实例图片", "./", "All Files (*)")
        name = filename.split("/")[-1]
        self.lable4.setText(name)

    def get_list(self):
        self.clearname = self.lable4.text()
        flag = self.lineedit4.text()
        num = self.lineedit5.text()
        for i in range(len(flag)):
            self.clearname = self.clearname.split(flag[i])[int(num[i])]
        self.lable7.setText(self.clearname)