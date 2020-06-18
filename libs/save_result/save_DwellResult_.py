from libs.read_bbox import read_bbox
import pandas as pd
class save_DwellResult_():
    def __init__(self, xml_dir, track_input, parameter, save_path):
        self.xml_dir = xml_dir
        self.track_input = track_input
        # self.bboxs = bboxs_input
        self.parameter = parameter
        self.save_path = save_path

    def save(self):
        all = self.track_input
        Data = []
        method_name = ""
        T = self.parameter[1]
        if self.parameter[0] == 0:
            method_name = "减第一帧"
        else:
            method_name = "逐帧递减"
            T = 1
        Data.append(["处理方法:", method_name])

        Data.append(["更新周期", T])
        Data.append(["ID", "First Frame", "Last Frame", "Dwell Time"])
        for i in range(len(all)):
            temp = []

            start_frame = all[i][1][0]
            over_frame = all[i][-1][0]
            if len(all[i][0]) == 4:
                for j in range(1, len(all[i])):
                    if len(all[i][j]) == 3:
                        over_frame = all[i][j][0]
                        break
            if self.parameter[0] == 1 and len(all[i]) == 2:
                continue  # 如果逐帧相减且只有起始点，则认为该点一直存在，将其走掉的frame设为最后一个frame
            elif len(all[i][0]) == 3 and self.parameter[0] == 0 and all[i][-1][0] % 500 == 0:
                continue  # 如果减第一帧，该轨迹的最后一帧是500的整数倍，那就认为该粒子还存在
            temp.append(i)
            temp.append(start_frame)
            temp.append(over_frame)
            temp.append(over_frame - start_frame)

            for j in range(len(all[i])):
                temp.append(all[i][j])

            Data.append(temp)

        df = pd.DataFrame(Data)
        print(df)
        writer = pd.ExcelWriter(self.save_path)  # 写入Excel文件
        df.to_excel(writer, 'page_1', float_format='%d', index=False)
        worksheet1 = writer.sheets["page_1"]
        worksheet1.set_column('A:D', 8)
        writer.save()
        writer.close()




    def get_central_point(self, bbox):
        return (bbox[3]+bbox[1]) // 2, (bbox[4]+bbox[2]) // 2


