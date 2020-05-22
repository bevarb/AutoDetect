from libs.read_bbox import read_bbox
import pandas as pd
class save_result_():
    def __init__(self, xml_dir, track_input, parameter, save_path):
        self.xml_dir = xml_dir
        self.track_input = track_input
        # self.bboxs = bboxs_input
        self.parameter = parameter
        self.save_path = save_path

    def save(self):
        all = self.track_input
        Data = []
        method = ""
        T = self.parameter[1]
        if self.parameter[0] == 0:
            method = "减第一帧"
        else:
            method = "逐帧递减"
        # Data.append(["处理方法:", method])
        # Data.append(["更新周期", T])
        Data.append(["ID", "First Frame", "Last Frame", "Dwell Time", "Trail Frame, [central_x, central_y]"])
        for i in range(len(all)):
            temp = []
            temp.append(i)
            temp.append(all[i][1][0])
            temp.append(all[i][-1][0])
            temp.append(all[i][-1][0] - all[i][1][0] + 1)
            for j in range(len(all[i]) - 1):
                frame = all[i][j + 1][0]
                box_id = all[i][j + 1][1]
                bbox = read_bbox.read(self.xml_dir + "/" + str(frame) + ".xml")
                [central_x, central_y] = self.get_central_point(bbox[box_id])
                temp.append([frame, [central_x, central_y]])
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


