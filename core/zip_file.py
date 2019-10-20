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
    def __init__(self, path):
        self.oldpath = os.path.split(os.path.split(os.path.split(path)[0])[0])[0] + "/core/README.md"
        self.path = path

    def crate_file(self):
        with zipfile.ZipFile(os.path.split(self.path)[0] + "/" + time.strftime("%d-%m-%Y") + ".zip", "w",
                             zipfile.ZIP_DEFLATED) as fzip:
            fzip.write(self.oldpath)
            fzip.close()

    def add_file(self, newpath, oldpath):
        with zipfile.ZipFile(os.path.split(self.path)[0] + "/" + time.strftime("%d-%m-%Y") + ".zip", "a",
                             zipfile.ZIP_DEFLATED) as fzip:
            oldfilename = str(oldpath).split("/")[-1]
            replaceFile(newpath, oldpath)
            oldpath2 = str(oldpath).split("/")[-1] + "/" + oldfilename
            fzip.write(oldpath)
            fzip.close()


if __name__ == "__main__":
    New = "D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/TDC_Timer_Pro.ma"
    Old = "D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.ma"
    replaceFile(New, Old)
    a = ZipFile(Old)
    a.add_file(New)
    print(os.getcwd())
