import cv2
import shutil
import os
# def change_name(root, save_root, begain, type):
#
#     name = os.listdir(root)
#     name = sorted(name, key=lambda x: int(x.split(".")[0]))
#     path = [root + "/" + na for na in name]
#     for i in range(len(name)):
#         new = str(begain + i) + type
#         new_path = save_root + "/" + new
#         shutil.move(path[i], new_path)
#         print(name[i], "have been changed for", new)
#
#
# root = "/home/user/wangxu_data/code/2-AutoDetect/mmdetection/data/VOCdevkit/0_2262/JPEGImages"
# save_root = "/home/user/wangxu_data/code/2-AutoDetect/mmdetection/data/VOCdevkit/VOC2007/JPEGImages"
# change_name(root, save_root, 1320, ".tif")


'''修改曾强师兄的数据'''
def change_name(root, save_root, begain, type):

    name = os.listdir(root)
    name = sorted(name, key=lambda x: int(x.split("_")[1]))
    path = [root + "/" + na for na in name]
    for i in range(len(name)):
        new = str(begain + i) + type
        new_path = save_root + "/" + new
        shutil.move(path[i], new_path)
        print(name[i], "have been changed for", new)


root = "/media/user/Seagate Expansion Drive/20200820/120mA,100ms,10ms_complementary MNP conc log11_100x dulited pbs_2_3/Pos0"
save_root = "/media/user/Seagate Expansion Drive/20200820/120mA,100ms,10ms_complementary MNP conc log11_100x dulited pbs_2_3/Pos0"
change_name(root, save_root, 20000, ".tif")