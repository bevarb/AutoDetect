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


root = "/home/user/wangxu_data/Data/To WangXu/aaa"
save_root = "/home/user/wangxu_data/Data/To WangXu/bbb"
change_name(root, save_root, 1200, ".xml")