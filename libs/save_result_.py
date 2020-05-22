
import pandas as pd
class save_result_():
    def __init__(self, input, parameter, save_path):
        self.input = input
        self.parameter = parameter
        self.save_path = save_path

    def save(self):
        all = self.input
        dwell_time = [[all[i][-1][0], all[i][1][0] + 1, all[i][-1][0] - all[i][1][0] + 1] for i in range(len(all))]

        df = pd.DataFrame(dwell_time)
        # df = df.T
        print(df)
        writer = pd.ExcelWriter(self.save_path)  # 写入Excel文件
        df.to_excel(writer, 'page_1', float_format='%d')
        writer.save()
        writer.close()


