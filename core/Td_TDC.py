# coding=utf-8
import os
import shutil
import AssetIO.core.Td_message as Td_message
import AssetIO.core.Td_filename as Td_filename
import AssetIO.core.zip_file as zipfile
import AssetIO.core.filrupdate as filrupdate
"""
文件夹结构以列表存储

"""

project_name = "TDC/"
assert_Type = ["Cha", "Env", "Pro"]
new_old_name = {}
new_old_name_message = {}

execcode = int(input("请输入你要执行的步骤："))


# 获取记录的内容并打印
# 调用Td_message,获取打印内容
a = Td_message.FolderMessage()
a.foldertraver("D:/school/TdClass/AssetIO/example/project/Inbox")
# 文件输出
a.printMessage()
filename, filepath = a.folderList()
# print(filename, filepath)

new_old_name_message = Td_filename.create_new_old(assert_Type, filepath, project_name)


# 创建目标文件与原始文件的字典
if execcode == 1:
    # 按照文件夹结构创建文件夹
    new_old_name = Td_filename.createfolder_newolddict(assert_Type, filepath, project_name)

# 将文件打包发回，发回时需要回归为甲方原有文件结构，并以代码执行时间为压缩包名称。
    # 构建函数，传入参数(Td_filename的返回值)，
    # 将更改过的文件替换之前存在的，并改变为原有结构
    # 对文件进行打包。并以执行时间为压缩包名称
    #
if execcode == 2:
    zip_file = zipfile.ZipFile()
    for key, value in new_old_name_message.items():
        zip_file.add_file(key, value)


# 对文件进行更新
if execcode == 3:
    # print(new_old_name_message)
    for key, value in new_old_name_message.items():
        # print(key, value)
        filrupdate.backup(key, value)