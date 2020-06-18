import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from libs.figure.figure_QDialog import fig_Dialog

class figure_DwellTime(QThread):

    def __init__(self, over_tracked, Method, parent=None):
        super(figure_DwellTime, self).__init__()
        self.overtracked = over_tracked
        self.Method = Method

    def process_(self):
        all = self.overtracked
        dwell_time = []
        for i in range(len(all)):
            start_frame = all[i][1][0]
            over_frame = all[i][-1][0]
            if len(all[i][0]) == 4:
                for j in range(1, len(all[i])):
                    if len(all[i][j]) == 3:
                        over_frame = all[i][j][0]
                        break
            if self.Method == 1 and len(all[i]) == 2:
                continue  # 如果逐帧相减且只有起始点，则认为该点一直存在，将其走掉的frame设为最后一个frame
            elif len(all[i][0]) == 3 and self.Method == 0 and all[i][-1][0] % 500 == 0:
                continue  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在

            dwell_time.append(over_frame - start_frame)

        result = pd.value_counts(dwell_time)
        x = list(result.index)
        x = sorted(x)
        y = [result[i] for i in x]
        plt.bar(range(len(y)), y, width=0.8, color='c', tick_label=x)
        plt.xticks(fontsize=7, rotation=30)
        plt.title("Histogram of binding dwell time", fontsize=10)
        plt.xlabel('Dwell Time, Frame')
        plt.savefig("./temp/temp_DwellTime.tif")
        plt.close()
        fig = fig_Dialog("./temp/temp_DwellTime.tif", "Histogram of binding-event")
        fig.start()

    def generate_img_Menu(self):
        self.menu = QMenu()
        self.change_index_Action = QAction(QIcon('resources/icons/open.png'), '&Change Index', self)
        self.change_index_Action.triggered.connect(self.change_index_)
        self.menu.addAction(self.change_index_Action)
        self.menu.popup(QCursor.pos())
        self.menu.show()

    def change_index_(self):
        dialog = QDialog()
        self.dialog = QDialog()
        self.dialog.setWindowTitle("设置曝光时间")
        self.dialog.resize(250, 100)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        lable1 = QLabel("处理格式:")
        lineedit1 = QLineEdit()
        layout1.addWidget(lable1)
        layout1.addWidget(lineedit1)
        Wid1 = QWidget()
        Wid1.setLayout(layout1)

        layout2 = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancle_btn = QPushButton("取消")
        layout2.addWidget(ok_btn)
        layout2.addWidget(cancle_btn)
        Wid2 = QWidget()
        Wid2.setLayout(layout2)

        layout.addWidget(Wid1)
        layout.addWidget(Wid2)
        dialog.setLayout(layout)
        dialog.show()
        ok_btn.clicked.connect(self.dialog.close)

        def _cancle():
            lineedit1.clear()
            dialog.close()

        cancle_btn.clicked.connect(_cancle)
        ret = dialog.exec_()

        if ret == 0:
            if len(lineedit1.text()) > 0:
                print(lineedit1.text())



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
