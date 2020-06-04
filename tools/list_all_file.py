
import os

def list_dir(path):
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    i = 0
    for file in listdir:
        os.rename(path+"/"+file, path+"/"+str(i)+"."+file.split(".")[-1])
        i += 1
    print(path + "have been list")

def delete_xml(delete_list, delete_path, flag):
    path = delete_path
    for de in delete_list:
        if os.path.exists(path+"/" + de + flag):
            os.remove(path + "/" + de + flag)
            print(str(de) + flag + "have been delete")
        else:
            print(str(de) + flag + " have been delete before")
def get_deletelist(img_path, flag):
    path = img_path
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    deletelist = []
    last = int(listdir[-1].split('.')[0])
    for i in range(last):
        if str(i) + flag in listdir:
            pass
        else:
            deletelist.append(str(i))
            print("add one delete file %s%s" % (str(i), flag))
    print('There have %d files need been delete' % len(deletelist))
    return deletelist
img_path = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/binding_tifs"
xml_path = "/home/user/wangxu_data/code/2-AutoDetect/VOC2007/binding_Annotations"
deletlist = get_deletelist(xml_path, ".xml")
delete_xml(deletlist, img_path, ".tif")
list_dir(img_path)
list_dir(xml_path)


