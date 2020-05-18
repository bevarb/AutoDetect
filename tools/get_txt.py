import os
import random

list = os.listdir("/home/user/wangxu_data/code/2-AutoDetect/mmdetection/data/VOCdevkit/VOC2007/Annotations")
random.shuffle(list)
len = len(list)
trainval = list[:int(0.9 * len)]

train_val_all = trainval.copy()
random.shuffle(train_val_all)
train = train_val_all[:int(0.8 * len)]
val = train_val_all[int(0.8 * len):int(0.9 * len)]

test = list[int(0.9 * len):len]
def get_txt(list, name):
    if not os.path.exists(name + ".txt"):
        os.mknod(name + ".txt")
    f1 = open(name + '.txt', 'w')
    for i in list:
        f1.write(i.split(".")[0] + "\n")
    f1.close()
get_txt(trainval, "trainval")
get_txt(train, "train")
get_txt(test, "test")
get_txt(val, "val")
