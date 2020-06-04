from libs.read_bbox import read_bbox
import pandas as pd
class save_DynamicResult_():
    def __init__(self, track_input, parameter, save_path):
        self.track_input = track_input
        # self.bboxs = bboxs_input
        self.parameter = parameter
        self.save_path = save_path
        self.binding = []
        self.debinding = []

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
            if len(all[i][0]) == 4:
                for j in range(1, len(all[i])):
                    if len(all[i][j]) == 3:
                        over_frame = all[i][j][0]
                        break
            self.binding.append(start_frame)
            self.debinding.append(over_frame)
        binding = self.sort_(self.binding)
        debinding = self.sort_(self.debinding)
        binding_Data = pd.DataFrame(binding, columns=["Frame", "New Binding"])
        binding_Data = binding_Data.set_index("Frame", drop=True)
        debinding_Data = pd.DataFrame(debinding, columns=["Frame", "New Debinding"])
        debinding_Data = debinding_Data.set_index("Frame", drop=True)

        df = pd.concat([binding_Data, debinding_Data], axis=1)
        print(df)
        writer = pd.ExcelWriter(self.save_path)  # 写入Excel文件
        df.to_excel(writer, 'page_1', float_format='%d')
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



