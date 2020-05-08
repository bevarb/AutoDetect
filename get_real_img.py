import cv2
import os
root = "/home/user/wangxu_data/Data/To WangXu/BSA"
name = os.listdir(root)
name = sorted(name, key=lambda x: int(x.split("_")[-1].split(".")[0]))
path = [root+"/"+na for na in name]
for i in range(len(path)-1):
    img1 = cv2.imread(path[i])
    img2 = cv2.imread(path[i+1])
    img = img2 - img1
    cv2.imwrite("/home/user/wangxu_data/Data/To WangXu/BSA_Clear/%d.tif" % (i+1), img)
