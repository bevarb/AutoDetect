import cv2
import shutil
import os
def change_name(root, save_root, begain, type):

    name = os.listdir(root)
    name = sorted(name, key=lambda x: int(x.split(".")[0]))
    path = [root + "/" + na for na in name]
    for i in range(len(name)):
        new = str(begain + int(name[i].split(".")[0])) + type
        new_path = save_root + "/" + new
        shutil.move(path[i], new_path)
        print(name[i], "have been changed for", new)


root = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/debinding_tifs"
save_root = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/111"
change_name(root, save_root, 1837, ".tif")