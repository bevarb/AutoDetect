import cv2
import os
import numpy as np
from PIL import Image
root = "/home/user/桌面/z-step_WangXu/Raw_Data_2"
save_root = "/home/user/桌面/z-step_WangXu/Clear_Data_2"
for i in range(4):
    dir_name = os.listdir(root)
    dir = root + "/" + dir_name[i]
    save_dir = save_root + "/" + dir_name[i]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    son_dir_list = os.listdir(dir)
    son_dir_list = sorted(son_dir_list, key=lambda x: int(x))
    for k in range(len(son_dir_list) - 1):
        First = dir + "/" + son_dir_list[k]
        son_dir = dir + "/" + son_dir_list[k+1]
        son_save_dir = save_dir + "/" + son_dir_list[k+1]
        if not os.path.exists(son_save_dir):
            os.makedirs(son_save_dir)

        First_name = os.listdir(First)
        First_name = sorted(First_name, key=lambda x: int(x.split("Z")[-1].split(".")[0]))

        source_name = os.listdir(son_dir)
        source_name = sorted(source_name, key=lambda x: int(x.split("Z")[-1].split(".")[0]))

        First_path = [First + "/" + name for name in First_name]
        source_path = [son_dir + "/" + name for name in source_name]
        for i in range(min(len(source_path), len(First_path))):
            print(First_path[i])
            print(source_path[i])
            if os.path.exists(First_path[i]) and os.path.exists(source_path[i]):
                # img1 = cv2.imread(First_path[i])
                # img2 = cv2.imread(source_path[i])
                img1 = np.array(Image.open(First_path[i]))
                img2 = np.array(Image.open(source_path[i]))
                img = img2 - img1
                img = cv2.bitwise_not(img)
                cv2.imwrite(son_save_dir + "/%d.tif" % (i + 1), img)

