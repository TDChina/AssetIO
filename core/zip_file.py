# coding=utf-8
import os
import shutil
import zipfile
import time
"""
传入参数：
new: D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/TDC_Timer_Pro.ma
old: D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.ma
执行操作：
1.将new中的文件替换old中的文件
2.将原始文件夹及进行打包，取名为脚本执行时间
"""


def replaceFile(new, old):
    os.remove(old)
    print("删除  %s" %old.split("/")[-1])
    shutil.copy(new, old)
    print("复制成功  %s" % old.split("/")[-1])


class ZipFile():
    def __init__(self):
        self.oldpath = "D:/school/TdClass/AssetIO/example/README.md"

    def crate_file(self):
        with zipfile.ZipFile("D:/school/TdClass/AssetIO/example/project/" + time.strftime("%d-%m-%Y") + ".zip", "w",
                             zipfile.ZIP_DEFLATED) as fzip:
            fzip.write(self.oldpath)
            fzip.close()

    def add_file(self, newpath, oldpath):
        with zipfile.ZipFile("D:/school/TdClass/AssetIO/example/project/" + time.strftime("%d-%m-%Y") + ".zip", "a",
                             zipfile.ZIP_DEFLATED) as fzip:
            oldfilename = str(oldpath).split("/")[-1]
            print(oldfilename)
            replaceFile(newpath, oldpath)
            oldpath2 = str(oldpath).split("/")[-1] + "/" + oldfilename
            # os.rename(oldpath,oldpath2)
            fzip.write(oldpath)
            fzip.close()


if __name__ == "__main__":
    New = "D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/TDC_Timer_Pro.ma"
    Old = "D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.ma"
    replaceFile(New, Old)
    a = ZipFile(Old)
    a.add_file(New)
    print(os.getcwd())
