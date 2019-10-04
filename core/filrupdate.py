# coding=utf-8
import os
import shutil
import time
import hashlib
"""
该函数被调用后，便会返回一个更新的路径列表
对比md5码，来找出被修改的文件
"""
New = "D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/TDC_Timer_Pro.txt"
old = 'D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.txt'


def md5compare(newpath, oldpath):
    with open(newpath, "rb") as f:
        data = f.read()
    newmd5 = hashlib.md5(data).hexdigest()

    with open(oldpath, "rb") as f:
        data = f.read()
    oldmd5 = hashlib.md5(data).hexdigest()
    return newmd5 != oldmd5


def backup(newpath, oldpath):
    print(md5compare(newpath, oldpath))
    if md5compare(newpath, oldpath):
        back_file = os.path.split(newpath)[0] + "/" + os.path.split(newpath)[1].split(".")[0] + "_" + \
                    time.strftime("%Y-%m-%d %H-%M-%S") + "." + os.path.split(newpath)[1].split(".")[1]
        print(back_file)
        shutil.move(newpath, back_file)
        shutil.copy(oldpath, newpath)
        print("更新成功  %s" % old.split("/")[-1])
    else:
        print("无需更新！！")


if __name__ == "__main__":
    backup(New, old)
