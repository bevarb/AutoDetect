
import os

def list_dir(path):
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    i = 0
    for file in listdir:
        os.rename(path+"/"+file, path+"/"+str(i)+"."+file.split(".")[-1])
        i += 1
    print(path + "have been list")

def delete_xml(delete_list):
    path = "Annotation"
    for de in delete_list:
        if os.path.exists(path+"\\"+de+".xml"):
            os.remove(path + "\\" + de + ".xml")
            print(str(de)+".xml have been delete")
        else:
            print(str(de) + ".xml have been delete before")
def get_deletelist():
    path = "Data"
    dir = os.listdir(path)
    listdir = sorted(dir, key=lambda x: int(x.split('.')[0]))
    deletelist = []
    last = int(listdir[-1].split('.')[0])
    for i in range(last):
        if str(i) + ".tif" in listdir:
            pass
        else:
            deletelist.append(str(i))
            print("add one delete file %s.tif" % (str(i)))
    return deletelist
deletlist = get_deletelist()
delete_xml(deletlist)
list_dir('Annotation')
list_dir('Data')



