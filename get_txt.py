import os
import random
list = os.listdir("Annotation")
random.shuffle(list)
len = len(list)
train = list[:int(0.8 * len)]
test = list[int(0.8 * len):int(0.95 * len)]
val = list[int(0.95 * len):len]
def get_txt(list, name):
    if not os.path.exists(name + ".txt"):
        os.mknod(name + ".txt")
    f1 = open(name + '.txt', 'w')
    for i in list:
        f1.write(i.split(".")[0] + "\n")
    f1.close()
get_txt(train, "train")
get_txt(test, "test")
get_txt(val, "val")
