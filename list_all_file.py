path = "Data"
import os
dir = os.listdir(path)
listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
deletelist=[]
def list_dir(path):
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    i = 0
    for file in listdir:
        os.rename(path+"/"+file, path+"/"+str(i)+"."+file.split(".")[-1])

def