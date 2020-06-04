import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from libs.figure.figure_QDialog import fig_Dialog
import os
class figure_DynamicTrack(QThread):

    def __init__(self, over_tracked, parent=None):
        super(figure_DynamicTrack, self).__init__()
        self.overtracked = over_tracked
        self.binding = []
        self.debinding = []

    def process_(self):
        all = self.overtracked

        for i in range(len(all)):
            start_frame = all[i][1][0]
            over_frame = all[i][-1][0]
            if len(all[i][0]) == 4:
                for j in range(1, len(all[i])):
                    if len(all[i][j]) == 3:
                        over_frame = all[i][j][0]
                        break
            self.binding.append(start_frame)
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
