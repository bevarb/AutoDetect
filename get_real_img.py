import cv2
import os
from PIL import Image
import numpy as np
root = "/home/user/wangxu_data/Data/To WangXu/BSA"
name = os.listdir(root)
name = sorted(name, key=lambda x: int(x.split("_")[-1].split(".")[0]))
path = [root+"/"+na for na in name]
d = 5
# for i in range((len(path)-1)//d - 1):
#     img1 = 0
#     for j in range(d):
#         temp = cv2.imread(path[i+j])//d
#         img1 += temp
#     img2 = 0
#     for j in range(d):
#         temp = cv2.imread(path[i+1+j])//d
#         img2 += temp
#     img = img2 - img1
#     cv2.imwrite("/home/user/wangxu_data/Data/To WangXu/test_d5/%d.tif" % (i+1), img)
for i in range(len(path) - 1):
    n = i // 500
    # img1 = np.array(Image.open(path[n * 500]))
    # img2 = np.array(Image.open(path[i + 1]))
    img1 = cv2.imread(path[n * 500])
    img2 = cv2.imread(path[i + 1])
    img = img2 - img1

    cv2.imwrite("/home/user/wangxu_data/Data/To WangXu/BSA_new_clear/%d.tif" % (i + 1), img)

