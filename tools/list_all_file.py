
import os
import cv2
import shutil

def change_name(root, save_root, begain, type):

    name = os.listdir(root)
    name = sorted(name, key=lambda x: int(x.split(".")[0]), reverse=True)  # 得到逆序的名字
    path = [root + "/" + na for na in name]
    for i in range(len(name)):
        current = int(name[i].split(".")[0])
        new = str(begain + current) + type
        new_path = save_root + "/" + new
        shutil.move(path[i], new_path)
        print(name[i], "have been changed for", new)

def list_dir(path):
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    i = 0
    for file in listdir:
        os.rename(path+"/"+file, path+"/"+str(i)+"."+file.split(".")[-1])
        i += 1
    print(path + "have been list")

def delete_xml(delete_list, delete_path, flag):
    '''根据删除列表进行删除'''
    path = delete_path
    for de in delete_list:
        if os.path.exists(path+"/" + de + flag):
            os.remove(path + "/" + de + flag)
            print(str(de) + flag + "have been delete")
        else:
            print(str(de) + flag + " have been delete before")


def get_deletelist(img_path, flag):
    '''获得需要删除的文件列表'''
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

def delete_more(img_path, xml_path):
    '''删除一些多的图片'''
    xml_name = os.listdir(xml_path)
    L = len(xml_name)
    img_name = os.listdir(img_path)
    img_name = sorted(img_name, key=lambda x: int(x.split(".")[0]))
    for i in range(L, len(img_name)):
        path = img_path + "/%d.tif" % i
        if os.path.exists(path):
            os.remove(path)
            print("Delete more tif : %d.tif" % i)

# 主函数
img_path = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/DATA7/Clear_T5"
xml_path = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/data_zch/DATA7/Train_XML_T5"
# 获得需要删除的名字索引
deletlist = get_deletelist(xml_path, ".xml")
# 删除文件
delete_xml(deletlist, img_path, ".tif")
# 对文件名字进行整理
list_dir(img_path)
list_dir(xml_path)
# 删除多的图片
delete_more(img_path, xml_path)
# 修改开始位置
target_xml_path = "/home/user/wangxu_data/code/2-AutoDetect/Train_Data/de_foucus/JPEGImages"
BEGAIN = len(os.listdir(target_xml_path))
change_name(img_path, img_path, BEGAIN, ".tif")
change_name(xml_path, xml_path, BEGAIN, ".xml")



