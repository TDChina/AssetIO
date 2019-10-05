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
# 初始化目标文件与原始文件的字典
new_old_name = {}
new_old_name_message = {}
# 获取记录的内容并打印
# 调用Td_message,获取对象
a = Td_message.FolderMessage()
# 对项目文件进行遍历操作
path1 = "D:/school/TdClass/AssetIO/example/project/Inbox"
a.foldertraver(path1)
# 打印输出
a.printMessage()
# 获取文件名、文件路径
filename, filepath = a.folderList()
# 获取键值对为目标文件原始文件的字典
new_old_name_message = Td_filename.create_new_old(assert_Type, filepath, project_name, path1)
# 选择执行的步骤
execcode = int(input("请输入你要执行的步骤："))

if execcode == 1:
    # 获取目标文件与原始文件的字典 并按照文件夹结构创建文件夹
    new_old_name = Td_filename.createfolder_newolddict(assert_Type, filepath, project_name, path1)

if execcode == 2:
    # 将文件打包发回，发回时需要回归为甲方原有文件结构，并以代码执行时间为压缩包名称。
    # 构建函数，传入参数(Td_filename的返回值)，
    # 将更改过的文件替换之前存在的，并改变为原有结构
    # 对文件进行打包。并以执行时间为压缩包名称
    zip_file = zipfile.ZipFile(path1)
    for key, value in new_old_name_message.items():
        zip_file.add_file(key, value)

if execcode == 3:
    # 对文件进行更新
    for key, value in new_old_name_message.items():
        print(key,value)
        filrupdate.backup(key, value)
