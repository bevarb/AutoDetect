from PIL import Image
import numpy as np
path = '/home/user/wangxu_data/code/2-AutoDetect/mmdetection/data/VOCdevkit/sub_before/JPEGImages/1017.tif'
a = Image.open(path)
a = np.array(a)
print(a)