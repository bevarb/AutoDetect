from libs.read_bbox import read_bbox
import pandas as pd
class save_DwellResult_():
    def __init__(self, xml_dir, track_input, parameter, save_path):
        self.xml_dir = xml_dir
        self.track_input = track_input
        # self.bboxs = bboxs_input
        self.parameter = parameter
        self.save_path = save_path
        self.max_Frame = 0
        for i in range(len(track_input)):
            if track_input[i][-1][0] > self.max_Frame:
                self.max_Frame = track_input[i][-1][0]

    def save(self):
        all = self.track_input
        Data = []
        #  将参数放入表格中，记录下来
        method_name = ""
        T = self.parameter[1]
        if self.parameter[0] == 0:
            method_name = "减第一帧"
        else:
            method_name = "逐帧递减"
            T = 1
        Data.append(["处理方法:", method_name])
        Data.append(["更新周期", T])
        Data.append(["ID", "First Frame", "Last Frame", "Dwell Time", "Intensity"])
        # 开始将数据记录
        for i in range(len(all)):
            temp = []

            start_frame = all[i][1][0]
            intensity = all[i][1][3]
            over_frame = all[i][-1][0]
            if all[i][-1][2] == "debinding":
                over_index = self.search_debinding(all[i])
                over_frame = all[i][over_index][0]
            # elif all[i][-1][2] == "binding":
            #     over_frame = self.max_Frame

                # for j in range(1, len(all[i])):
                #     if len(all[i][j]) == 3:
                #         over_frame = all[i][j][0]
                #         break

            if self.parameter[0] == 1 and len(all[i]) == 2:
                pass
                # over_frame = self.max_Frame  # 如果逐帧相减且只有起始点，则认为该点一直存在
            elif self.parameter[0] == 0 and all[i][-1][2] == "binding" and all[i][-1][0] % T == 0:
                pass
                # over_frame = self.max_Frame  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在

            temp.append(i)
            temp.append(start_frame)
            temp.append(over_frame)
            temp.append(over_frame - start_frame)
            temp.append(intensity)

            for j in range(len(all[i])):
                temp.append(all[i][j])

            Data.append(temp)

        df = pd.DataFrame(Data)
        print(df)
        writer = pd.ExcelWriter(self.save_path)  # 写入Excel文件
        df.to_excel(writer, 'page_1', float_format='%d', index=False)
        worksheet1 = writer.sheets["page_1"]
        worksheet1.set_column('A:F', 10)
        worksheet1.set_column('G:S', 22)
        writer.save()
        writer.close()

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


    def get_central_point(self, bbox):
        return (bbox[3]+bbox[1]) // 2, (bbox[4]+bbox[2]) // 2


