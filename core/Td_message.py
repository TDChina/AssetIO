# coding=utf-8
import os
import re
import time
"""
#通过调用该函数来获取
#1.收到文件的时间：文件在本地创建的时间
#2.文件的数量
#3.文件的内容
# 打印示例
*************Message****************
收到文件时间：-dd -mm -yy
收到文件数量：xx
文件的内容：
角色：xx个，name1,name2
场景：xx个，name1,name2
道具：xx个，name1,name2
函数输出：文件名(列表)，文件路径+含文件名(列表)
"""


class FolderMessage():

    def __init__(self):
        # 初始化文件夹路径，文件夹列表
        self.path_name = [[], [], []]
        self.file_name = []
        self.numtotal = 0
        self.chaname, self.envname, self.proname = [], [], []
        self.messages = []

    def foldertraver(self, path):
        folders = os.listdir(path)
        for folder in folders:
            # 判断是否为文件夹
            if os.path.isdir(path + "/" + str(folder)):
                path = path + "/" + str(folder)
                # folder = os.listdir(self.path)
                self.foldertraver(path)

            # 如果是文件夹则进行深层遍历
            elif os.path.isdir(os.path.split(path)[0] + "/" + folder):
                path = os.path.split(path)[0] + "/" + folder
                self.foldertraver(path)

            else:
                self.numtotal += 1
                self.addMessage(folder + ":  " + time.ctime(os.path.getmtime(path + "/" + folder)))

                # self.file_name.append(os.path.split(path)[0] + "\\" + folder)
                if folder.split("_")[-1].split(".")[0] == "cha":
                    self.chaname.append(folder)
                    self.path_name[0].append(path + "/" + folder)
                elif folder.split("_")[-1].split(".")[0] == "env":
                    self.envname.append(folder)
                    self.path_name[1].append(path + "/" + folder)
                elif folder.split("_")[-1].split(".")[0] == "pro":
                    self.proname.append(folder)
                    self.path_name[2].append(path + "/" + folder)

    def addMessage(self, message):
        self.messages.append(message)

    def folderList(self):
        self.file_name.append(self.chaname)
        self.file_name.append(self.envname)
        self.file_name.append(self.proname)
        return self.file_name, self.path_name

    def printMessage(self):
        print("*************Message****************\n************************************")
        for message in self.messages:
            print(message)
        print("The file of the folder count is: %d" % self.numtotal)
        print("The file include:")
        print("  character: %d个" % len(self.chaname))
        for charfile in self.chaname:
            print("     " + charfile)
        print("  env: %d个" % len(self.envname))
        for envfile in self.envname:
            print("     " + envfile)
        print("  prop: %d个" % len(self.proname))
        for propfile in self.proname:
            print("     " + propfile)


if __name__ == "__main__":
    a = FolderMessage()
    a.foldertraver("D:/school/TdClass/AssetIO/example/project/Inbox")
    # 文件输出
    a.printMessage()
    filename, filepath = a.folderList()
    print(filename)
    print(filepath)

