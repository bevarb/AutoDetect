from libs.read_bbox import read_bbox
import pandas as pd
import numpy as np
class save_DynamicResult_():
    def __init__(self, track_input, parameter, save_path):
        self.track_input = track_input
        # self.bboxs = bboxs_input
        self.parameter = parameter
        self.save_path = save_path
        self.binding = []
        self.debinding = []
        self.SubImg_T = parameter[1]

    def save(self):
        all = self.track_input
        # method = ""
        # T = self.parameter[1]
        # if self.parameter[0] == 0:
        #     method = "减第一帧"
        # else:
        #     method = "逐帧递减"
        # Data.append(["处理方法:", method])
        # Data.append(["更新周期", T])

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
            if self.parameter[0] == 1 and len(all[i]) == 2:
                over_frame = None  # 如果逐帧相减且只有起始点，则认为该点一直存在，将其走掉的frame设为最后一个frame
            elif self.parameter[0] == 0 and all[i][-1][2] == "binding" and all[i][-1][0] % self.SubImg_T == 0:
                over_frame = None  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在
            self.binding.append(start_frame)
            if over_frame != None:
                self.debinding.append(over_frame)
        binding = self.sort_(self.binding)
        debinding = self.sort_(self.debinding)
        binding_Data = pd.DataFrame(binding, columns=["Frame", "New Binding"])
        binding_Data = binding_Data.set_index("Frame", drop=True)
        debinding_Data = pd.DataFrame(debinding, columns=["Frame", "New Debinding"])
        debinding_Data = debinding_Data.set_index("Frame", drop=True)

        df = pd.concat([binding_Data, debinding_Data], axis=1)

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
            have_binding.append([i+1, b_])
            have_debinding.append([i+1, deb_])
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
                return index
        if abs(index) >= len(data):
            return -1
        return -1



