from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2 as cv
class fig_Dialog(QThread):

    def __init__(self, img_path, window_name, parent=None):
        super(fig_Dialog, self).__init__()
        self.img_path = img_path
        self.windowname = window_name
    def __del__(self):
        self.wait()

    def run(self):

        self.img = cv.imread(self.img_path)
        self.dialog = QDialog()
        self.dialog.setWindowTitle(self.windowname)
        self.dialog.resize(900, 700)
        layout = QHBoxLayout()
        pix1 = QLabel()
        pix1.setFixedSize(900, 500)
        if self.img.shape[0] > 800 or self.img.shape[1] > 500:
            ratio = self.img.shape[1] / self.img.shape[0]
            self.img = cv.resize(self.img, (int(ratio * 500), 500), interpolation=cv.INTER_CUBIC)
            pix1.setPixmap(self.cv2pixmap(self.img))
        else:
            pix1.setPixmap(self.cv2pixmap(self.img))
        pix1.setAlignment(Qt.AlignCenter)
        # pix1.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        # pix1.customContextMenuRequested.connect(self.generate_img_Menu)  # 右键菜单
        # pix1.setScaledContents(True)
        pix1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layout.addWidget(pix1)
        self.dialog.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.dialog.setLayout(layout)
        self.dialog.show()


    def cv2pixmap(self, img1):
        '''将cv图像转化维pixmap'''
        img = img1.copy()
        if len(img.shape) == 2:
            img = self._vec_(img1)
        height, width, channel = img.shape[0:3]
        bytesPerline = 3 * width
        Qimg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(Qimg)
        return pixmap
