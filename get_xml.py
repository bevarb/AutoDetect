import os
import shutil
Source_root = "D:\Project_Data\First\Clear_data"
Target_path = "D:\Project_Data\First\Clear_data\Annotation"
flag = 0
for i in range(15):
    Source_path = Source_root + "\\" + ("class_%d_xml" % i)
    xml = os.listdir(Source_path)
    list_xml = sorted(xml, key=lambda x: int(x.split('\\')[-1].split('_')[0]))
    for xml_ in list_xml:
        shutil.copy(Source_path+"\\"+xml_, Target_path+"\\"+str(flag)+".xml")
        flag += 1
