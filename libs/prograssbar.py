from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class proBar(QThread):
    quick_sig = pyqtSignal(int)
    def __init__(self, title, parent=None):
        super(proBar, self).__init__()
        self.title = title
    def __del__(self):
        self.wait()

    def run(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle(self.title + "...， Please wait!")
        self.dialog.resize(350, 100)
        layout = QHBoxLayout()
        wid = QWidget()
        self.progressBar = QProgressBar(wid)
        self.progressBar.setGeometry(QRect(20, 20, 250, 80))
        self.quick_btn = QPushButton("Quick")
        layout.addWidget(self.progressBar)
        layout.addWidget(self.quick_btn)
        self.dialog.setLayout(layout)
        self.quick_btn.clicked.connect(self.quick_detect)
        self.quick_flag = 0
        self.dialog.show()

    def quick_detect(self):
        self.quick_sig.emit(1)
        import time
        time.sleep(0.1)
        self.dialog.close()
    def set_value(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.dialog.close()