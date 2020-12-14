import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from libs.figure.figure_QDialog import fig_Dialog
import os
import numpy as np
class save_DynamicResult_(QThread):

    def __init__(self, over_tracked, parameter, save_path, parent=None):
        super(save_DynamicResult_, self).__init__()
        self.overtracked = over_tracked
        self.particle = {"binding":[], "debinding":[]}
        self.parameter = parameter
        self.save_path = save_path
        self.binding = []
        self.debinding = []
        self.Method = parameter[0]
        self.SubImg_T = parameter[1]

    def save(self):
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
        print(self.binding)
        binding = self.sort_(self.binding)
        debinding = self.sort_(self.debinding)
        binding_Data = pd.DataFrame(binding, columns=["Frame", "New Binding"])
        binding_Data = binding_Data.set_index("Frame", drop=True)
        debinding_Data = pd.DataFrame(debinding, columns=["Frame", "New Debinding"])
        debinding_Data = debinding_Data.set_index("Frame", drop=True)

        df = pd.concat([binding_Data, debinding_Data], axis=1)
        print(df)

        max_index = df.index[-1]
        index = [i for i in range(1, max_index + 1)]
        data = np.zeros([max_index, 2])
        for i in df.index:
            data[i - 1, :] = df.loc[i, :]
        new = pd.DataFrame(data, index=index, columns=["New Binding", "New Debinding"])
        new = new.fillna(0)
        have_binding = [[1, 0]]
        have_debinding = [[1, 0]]
        b_, deb_ = 0, 0
        for i in range(1, len(new)):
            b_ += new.iloc[i]["New Binding"]
            deb_ += new.iloc[i]["New Debinding"]
            have_binding.append([i + 1, b_])
            have_debinding.append([i + 1, deb_])
        have_binding_Data = pd.DataFrame(have_binding, columns=["Frame", "have Binding"])
        have_binding_Data = have_binding_Data.set_index("Frame", drop=True)
        have_debinding_Data = pd.DataFrame(have_debinding, columns=["Frame", "have Debinding"])
        have_debinding_Data = have_debinding_Data.set_index("Frame", drop=True)
        have_ = pd.concat([have_binding_Data, have_debinding_Data], axis=1)
        add_have = pd.concat([new, have_], axis=1)

        # print(df)
        writer = pd.ExcelWriter(self.save_path)  # 写入Excel文件
        add_have.to_excel(writer, 'page_1', float_format='%d')
        worksheet1 = writer.sheets["page_1"]
        worksheet1.set_column('A:D', 13)
        writer.save()
        writer.close()

    def sort_(self, result):
        result = pd.value_counts(result)
        x = list(result.index)
        x = sorted(x)
        sorted_ = [[i, result[i]] for i in x]

        return sorted_

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





