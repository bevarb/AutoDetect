from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class set_Detect(QDialog):
    set_Detect_sig = pyqtSignal(str, float, int)
    def __init__(self, model_path, parent=None):
        super(set_Detect, self).__init__()
        self.model_name = model_path.split("/")[-1]
        self.model_path = model_path

    def show_(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("选择加载模型")
        self.dialog.resize(350, 100)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel("模型:")
        self.lable12 = QLabel(self.model_name)
        btn1 = QPushButton("Load model")
        btn1.clicked.connect(self.load_model)
        layout1.addWidget(lable1)
        layout1.addWidget(self.lable12)
        layout1.addWidget(btn1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        lable21 = QLabel("阈值:")
        self.lineedit21 = QLineEdit("0.5")
        self.checkbox21 = QCheckBox("is search central")
        self.checkbox21.setChecked(True)

        layout2.addWidget(lable21)
        layout2.addWidget(self.lineedit21)
        layout2.addWidget(self.checkbox21)
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
            self.dialog.close()
            is_search_central = 1 if self.checkbox21.isChecked() else 0
            self.set_Detect_sig.emit(self.model_path,
                                     float(self.lineedit21.text()),
                                     int(is_search_central)
                                     )


        cancle_btn.clicked.connect(_cancle)
        ok_btn.clicked.connect(_ok)

    def load_model(self):
        filt = 'modelFile(*.pth)'
        model_path, filtUsed = QFileDialog.getOpenFileName(None, "加载模型",
                                "/home/user/wangxu_data/code/2-AutoDetect/AutoDetect/work_dirs/New", filt)
        if model_path != "":
            self.model_name = self.model_path.split("/")[-1]
            self.lable12.setText(self.model_name)
            self.model_path = model_path






