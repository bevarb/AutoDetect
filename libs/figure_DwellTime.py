import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2 as cv
# class Niiii(QLabel):                                        # 改动
#     x0 = 0
#     y0 = 0
#     x1 = 0
#     y1 = 0
#
#     flag = 0
#
#     def mousePressEvent(self, event):
#         '''鼠标单击事件'''
#         if T1 < event.x() < T2 and T3 < event.y() < T4:      # 改动
#             self.x0 = event.x()
#             self.y0 = event.y()
#         else:
#             pass
#
#
#
#     def mouseReleaseEvent(self, event):
#         '''鼠标释放事件'''
#         if T1 < event.x() < T2:
#             self.x1 = event.x()
#         elif event.x() <= T1:
#             self.x1 = T1
#         else:
#             self.x1 = T2
#         if T3 < event.y() < T4:
#             self.y1 = event.y()
#         elif event.y() <= T3:
#             self.y1 = T3
#         else:
#             self.y1 = T4
#
#         if self.flag == 1:
#             pqscreen = QGuiApplication.primaryScreen()
#             pixmap2 = pqscreen.grabWindow(self.winId(), self.A + 1, self.B + 1, abs(self.C) - 1, abs(self.D) - 1)
#             pixmap2.save('after_cut_img.png')
#         else:
#             pass
#         # pqscreen = QGuiApplication.primaryScreen()
#         # pixmap2 = pqscreen.grabWindow(self.winId(), self.A + 1, self.B + 1, abs(self.C) - 1, abs(self.D) - 1)
#         # pixmap2.save('after_cut_img.png')
#
#
#     def mouseMoveEvent(self, event):
#         '''鼠标移动事件'''
#         if T1 < event.x() < T2:
#             self.x1 = event.x()
#         elif event.x() <= T1:
#             self.x1 = T1
#         else:
#             self.x1 = T2
#         if T3 < event.y() < T4:
#             self.y1 = event.y()
#         elif event.y() <= T3:
#             self.y1 = T3
#         else:
#             self.y1 = T4
#         self.update()
#
#     ratio_sig = pyqtSignal(float)
#     norm_ratio = 1
#     def wheelEvent(self, event):
#         '''鼠标滚动事件'''
#         angle = event.angleDelta() / 10      # 返回QPoint对象，为滚轮转过的数值，单位为1/10度
#         angleY = angle.y()                   # 竖直滚过的距离
#         if angleY > 0:
#             self.norm_ratio += 0.2
#             if self.norm_ratio >= 4:
#                 self.norm_ratio = 4
#             else:
#                 pass
#             ratio = self.norm_ratio
#             #print("鼠标滚轮上滚", self.i)     # 响应测试语句
#         else:  # 滚轮下滚
#             self.norm_ratio -= 0.2
#             if self.norm_ratio <= 0:
#                 self.norm_ratio = 0.01
#             else:
#                 pass
#             ratio = self.norm_ratio
#             #print("鼠标滚轮下滚", self.i)     # 响应测试语句
#         self.ratio_sig.emit(float(ratio))
#     def receive(self, dec):
#         self.flag = dec
#         return self.flag
#
#     def paintEvent(self, event):
#         '''绘图事件'''
#         if self.flag == 1:                  # 改动
#             super().paintEvent(event)
#             '''四种情况下矩形的左上角与右下角'''
#             if self.x0 < self.x1 and self.y0 < self.y1:
#                 rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
#             elif self.x1 < self.x0 and self.y1 > self.y0:
#                 rect = QRect(self.x1, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
#             elif self.y0 > self.y1 and self.x1 > self.x0:
#                 rect = QRect(self.x0, self.y1, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
#             else:
#                 rect = QRect(self.x1, self.y1, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
#
#             painter = QPainter(self)
#             painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
#             painter.drawRect(rect)                                             # 重绘
#
#             self.A, self.B, self.C, self.D = list(rect.getRect())
#
#         else:             # 改动
#             super().paintEvent(event)

class figure_DwellTime(QThread):
    progressBarValue = pyqtSignal(int)
    def __init__(self, over_tracked, parent=None):
        super(figure_DwellTime, self).__init__()
        self.overtracked = over_tracked
    def __del__(self):
        self.wait()

    def run(self):
        all = self.overtracked
        dwell_time1 = [all[i][-1][0] - all[i][1][0] + 1 for i in range(len(all))]
        dwell_time = []  # 暂时将图像中为一帧的隐藏
        for i in range(len(dwell_time1)):
            if dwell_time1[i] != 1:
                dwell_time.append(dwell_time1[i])
        result = pd.value_counts(dwell_time)
        x = list(result.index)
        y = [result[i] for i in x]
        plt.bar(range(len(y)), y, width=0.8, color='c', tick_label=x)
        plt.xticks(fontsize=7, rotation=30)
        plt.title("Histogram of binding dwell time", fontsize=10)
        plt.xlabel('Dwell Time, Frame')
        plt.savefig("temp_DwellTime.tif")
        self.img = cv.imread("temp_DwellTime.tif")
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Figure")
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
    # def wheel_resize(self, ratio):
    #
    #     '''并重新设置'''
    #     img = self.img
    #
    #     # img列表中最新的，需要调整
    #     img = cv.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)), interpolation=cv.INTER_CUBIC)
    #
    #
    #     nowheight=img.shape[0]
    #     nowwidth=img.shape[1]
    #     #print('图长：', self.nowheight, '图宽：', self.nowwidth)
    #     global T1, T2, T3, T4
    #     if nowwidth <= self.wid:
    #         T1 = (self.wid - nowwidth) / 2
    #         T2 = (self.wid - nowwidth) / 2 + nowwidth
    #     else:
    #         T1 = 0
    #         T2 = self.wid
    #     if nowheight <= self.hei:
    #         T3 = (self.hei - nowheight) / 2
    #         T4 = (self.hei - nowheight) / 2 + nowheight
    #     else:
    #         T3 = 0
    #         T4 = self.hei
    #
    #     self.dialog.setPixmap(self.cv2pixmap(img))
