import cv2
import shutil
import os
def change_name(root, save_root, begain, type):

    name = os.listdir(root)
    name = sorted(name, key=lambda x: int(x.split(".")[0]))
    path = [root + "/" + na for na in name]
    for i in range(len(name)):
        new = str(begain + i) + type
        new_path = save_root + "/" + new
        shutil.move(path[i], new_path)
        print(name[i], "have been changed for", new)

# BEGAIN = 0
# root_XML = "/home/user/wangxu_data/code/2-AutoDetect/yolov4-pytorch/VOCdevkit/VOC2007/JPEGImages"
# save_root_XML = "/home/user/wangxu_data/code/2-AutoDetect/yolov4-pytorch/VOCdevkit/VOC2007/JPEGImages"
# change_name(root_XML, save_root_XML, BEGAIN, ".tif")
#
# root_XML = "/home/user/wangxu_data/code/2-AutoDetect/yolov4-pytorch/VOCdevkit/VOC2007/Annotations"
# save_root_XML = "/home/user/wangxu_data/code/2-AutoDetect/yolov4-pytorch/VOCdevkit/VOC2007/Annotations"
# change_name(root_XML, save_root_XML, BEGAIN, ".xml")

BEGAIN = 310
DATA = "DATA1"
root_XML = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/%s/Clear_T5" % DATA
save_root_XML = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/%s/Clear_T5" % DATA
change_name(root_XML, save_root_XML, BEGAIN, ".tif")

root_XML = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/%s/Train_XML_T5" % DATA
save_root_XML = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/%s/Train_XML_T5" % DATA
change_name(root_XML, save_root_XML, BEGAIN, ".xml")


# '''修改曾强师兄的数据'''
# def change_name(root, save_root, begain, type):
#
#     name = os.listdir(root)
#     name = sorted(name, key=lambda x: int(x.split("_")[1]))
#     path = [root + "/" + na for na in name]
#     for i in range(len(name)):
#         new = str(begain + i) + type
#         new_path = save_root + "/" + new
#         shutil.move(path[i], new_path)
#         print(name[i], "have been changed for", new)
#
#
# root = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_for_zq/DATA2/CLear_T3"
# save_root = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_for_zq/DATA2/CLear_T3"
# change_name(root, save_root, 212, ".tif")