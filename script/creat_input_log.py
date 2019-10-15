# -*- coding: utf-8 -*-
# .@FileName:creat_input_log
# @Date....:2019-10-04  07:28   
# ..:XingLian
# import datetime
import json
import os
import re
from script import get_files_list
# 按照时间遍历
# {asscet_name:[{version:(time,episode,asscet_typ)}...]

# 接收日期文件夹，接收文件存放绝对路径，log路径
def record_input_log(data, ipath, log_path):
    # 判断json是否存在
    # 如果存在，读取内容，如果不存在，创建一个
    json_path = rf'{log_path}\asscet_log.json'
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            assect_dict = json.load(f)
    else:
        f = open(json_path, 'w')
        f.close()
        assect_dict = {}

    # 遍历data文件夹获取episode
    episode_list = os.listdir(rf'{log_path}\{data}')
    for episode in episode_list:

        # 遍历episode文件夹获取资产名称
        asscet_list = os.listdir(rf'{log_path}\{data}\{episode}')
        for asscet in asscet_list:
            asscet = os.listdir(rf'{log_path}\{data}\{episode}\{asscet}')
            # 遍历，正则匹配，防止有多余垃圾文件
            for x in asscet:
                # 切割资产名称，获取资产版本信息存储到列表
                file_name = re.search(r'ep\d{2}_[a-z]+_(?:env|cha|pro)\.ma', x, re.I).group()
                episode, asscet, typ, _ = re.split(r'_|.ma', file_name)
            with open(rf'{log_path}\{i}.json', 'r+') as f:
                assect_dict[asscet].append
        # 将新的字典写入json中
        with open(rf'{log_path}\{i}.json', 'r+') as f:

            json.dump(assect_dict, f)


ipath = r'Z:\example\project\Inbox'
log_path = r'Z:\log'
data = os.listdir(ipath)

for i in data:
    record_input_log(i)