import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from libs.figure.figure_QDialog import fig_Dialog
import os
class figure_DynamicTrack(QThread):

    def __init__(self, over_tracked, method, T, parent=None):
        super(figure_DynamicTrack, self).__init__()
        self.overtracked = over_tracked
        self.particle = {"binding":[], "debinding":[]}
        self.binding = []
        self.debinding = []
        self.Method = method
        self.SubImg_T = T

    def process_(self):
        all = self.overtracked

        for i in range(len(all)):
            if self.Method == 0:
                start_frame = all[i][1][0]
                over_frame = all[i][-1][0]
                if all[i][-1][2] == "debinding":
                    over_index = self.search_debinding(all[i])
                    over_frame = all[i][over_index][0]

                if self.Method == 0 and all[i][-1][2] == "binding" and all[i][-1][0] % self.SubImg_T == 0:
                    # TODO:这里需要修改！！！
                    pass  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在
                self.binding.append(start_frame)
                self.debinding.append(over_frame)
            else:
                if len(all[i]) == 2:

                    # 如果这一类只有一个，可能为binding也可能为debinding，那就添加进去
                    if all[i][-1][2] != "debinding":
                        self.particle[all[i][-1][2]].append(all[i][-1][0])
                    pass
                # 下面是类别中大于2个的，标准为binding开始,debinding结束,不标准的则是binding开始，binding结束，
                start_frame = all[i][1][0]
                over_frame = all[i][-1][0]
                over_index = -1
                if all[i][-1][2] == "debinding":
                    over_index = self.search_debinding(all[i])
                    over_frame = all[i][over_index][0]
                self.particle["binding"].append(start_frame)
                self.particle["debinding"].append(over_frame)

                # if all[i][-1][2] == "debinding":
                #     over_index = self.search_debinding(all[i])
                #     over_frame = all[i][over_index][0]
                # if all[i][-1][2] == "binding" and all[i][over_index][2] == "debinding":
                #     self.particle["binding"].append(start_frame)
                #     self.particle["debinding"].append(over_frame)
                # elif all[i][-1][2] == "binding" and all[i][over_index][2] == "binding":
                #     self.particle["binding"].append(start_frame)
                # elif all[i][-1][2] == "debinding" and all[i][over_index][2] == "debinding":
                #     self.particle["debinding"].append(over_frame)
        if self.Method == 1:
            self.binding = self.particle["binding"]
            self.debinding = self.particle["debinding"]
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
                return index + 1
        if abs(index) >= len(data):
            return -1
        return -1
