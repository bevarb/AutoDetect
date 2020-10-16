import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from libs.figure.figure_QDialog import fig_Dialog
import os
class figure_DynamicTrack(QThread):

    def __init__(self, over_tracked, method, T, parent=None):
        super(figure_DynamicTrack, self).__init__()
        self.overtracked = over_tracked
        self.binding = []
        self.debinding = []
        self.Method = method
        self.SubImg_T = T

    def process_(self):
        all = self.overtracked

        for i in range(len(all)):
            start_frame = all[i][1][0]
            over_frame = all[i][-1][0]
            if all[i][-1][2] == "debinding":
                over_index = self.search_debinding(all[i])
                over_frame = all[i][over_index][0]
            # if len(all[i][0]) == 4:
            #     for j in range(1, len(all[i])):
            #         if len(all[i][j]) == 3:
            #             over_frame = all[i][j][0]
            #             break
            if self.Method == 1 and len(all[i]) == 2:
                over_frame = None  # 如果逐帧相减且只有起始点，则认为该点一直存在，将其走掉的frame设为最后一个frame
            elif self.Method == 0 and all[i][-1][2] == "binding" and all[i][-1][0] % self.SubImg_T == 0:
                over_frame = None  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在
            self.binding.append(start_frame)
            if over_frame != None:
                self.debinding.append(over_frame)
        x_binding, y_binding = self.get_x_y(self.binding)
        x_debinding, y_debinding = self.get_x_y(self.debinding)


        plt.plot(x_binding, y_binding, 'k-', label="Total Binding")
        plt.plot(x_debinding, y_debinding, 'r:', label="Total De-Binding")

        plt.title("Dynamic Tracking", fontsize=10)
        plt.xlabel('Time, Frame')
        plt.ylabel('Counts')
        plt.legend()
        os.makedirs("temp", exist_ok=True)
        plt.savefig("./temp/temp_Dynamic_Track.tif")
        plt.close()
        fig = fig_Dialog("./temp/temp_Dynamic_Track.tif", "Dynamic Track")
        fig.start()

    def get_x_y(self, result):
        result = pd.value_counts(result)
        x = list(result.index)
        x = sorted(x)
        y = []
        temp = 0
        for i in x:
            temp += result[i]
            y.append(temp)
        return x, y

    def search_debinding(self, data):
        '''从后往前搜索，找到第一次出现debinding的位置，则认为从这里结束,返回位置'''
        index = -1
        if data[1][2] == "debinding":
            return 1
        for i in range(2, len(data)):
            index = -1 * i
            if data[index][2] == "binding" and data[index + 1][2] == "debinding":
                return index
        if abs(index) >= len(data):
            return -1
        return -1
