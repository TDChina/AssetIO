# -*- coding: utf-8 -*-
# .@FileName:creat_input_log
# @Date....:2019-10-04  07:28   
# ..:XingLian
# import datetime
import json
import os


def get_files_list(file_dir, mode='files'):
    files_full_path = []
    folders_full_path = []
    if os.path.isfile(file_dir):
        if mode in ['files']:
            files_full_path.append(file_dir.replace('\\', '/'))
            return files_full_path
        return []
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        folders_full_path.extend([(root + '\\' + fl).replace('\\', '/') for fl in dirs])
        files_full_path.extend([(root + '\\' + f).replace('\\', '/') for f in files])
    if mode in ['files']:
        return files_full_path
    if mode in ['folders']:
        return folders_full_path
    else:
            return files_full_path + folders_full_path


def record_input_log(ipath=r'Z:\example\project\Inbox', log_path=r'Z:\log'):
    data = os.listdir(ipath)

    for i in data:
        dict = {}
        episode = os.listdir(rf'{ipath}\{i}')
        for x in episode:
            assect = os.listdir(rf'{ipath}\{i}\{x}')
            dict[x] = assect
        with open(rf'{log_path}\{i}.json', 'w') as f:
            print(dict)
            json.dump(dict, f)
record_input_log()