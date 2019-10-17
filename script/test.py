# -*- coding: utf-8 -*-
# .@FileName:test
# @Date....:2019-10-18  00:08   
# ..:XingLian
# a = [{0:''}]
#
# while True:
#     ver = list(a[-1].keys())[-1]
#     a.append({ver:len(a)})
#     print(a)
#     if len(a) > 100:
#         break

# -*- coding: utf-8 -*-
# .@FileName:creat_input_log
# @Date....:2019-10-04  07:28
# ..:XingLian
# import datetime
"""
创建两个json文件记录资产信息，
一个以资产名称为索引，记录版本信息，
一个以文件接收日期为索引，记录当天接收文件的内容
为了查找文件两种检索方式都不需要以遍历所有资产的方式进行
"""

# -*- coding: utf-8 -*-
# .@FileName:creat_input_log
# @Date....:2019-10-04  07:28
# ..:XingLian
# import datetime
"""
创建两个json文件记录资产信息，
一个以资产名称为索引，记录版本信息，
一个以文件接收日期为索引，记录当天接收文件的内容
为了查找文件两种检索方式都不需要以遍历所有资产的方式进行
"""

import json
import os
import re


# 接收日期文件夹，接收文件存放绝对路径，log路径
def record_input_log(data, ipath, log_path):
    # 判断asscet_log是否存在
    # 如果存在，读取内容，如果不存在，创建一个
    asscet_json = rf'{log_path}\asscet_log.json'
    if os.path.exists(asscet_json):
        with open(asscet_json, 'r') as f:
            assect_dict = json.load(f)
    else:
        f = open(asscet_json, 'w')
        f.close()
        assect_dict = {'asscet_name': [{0: {'time': '', 'episode': '', 'asscet_typ': ''}}]}

    # 判断receive_log是否存在
    # 如果存在，读取内容，如果不存在，创建一个
    receive_json = rf'{log_path}\receive_log.json'
    if os.path.exists(receive_json):
        with open(receive_json, 'r') as f:
            time_dict = json.load(f)
    else:
        f = open(receive_json, 'w')
        f.close()
        # 字典格式
        time_dict = {'time': {'episode': ['asscet_name']}}

    # 依次向下遍历，获取资产名称
    episode_list = os.listdir(rf'{ipath}\{data}')
    for episode in episode_list:
        asscet_list = os.listdir(rf'{ipath}\{data}\{episode}')
        for asscet_dir in asscet_list:
            asscet_name = os.listdir(rf'{ipath}\{data}\{episode}\{asscet_dir}')[0]

            # 正则匹配，防止有多余垃圾文件
            file_name = re.search(r'ep\d{2}_[a-z]+_(?:env|cha|pro)\.ma', asscet_name, re.I).group()
            # 切割资产名称，获取资产版本信息存储到列表
            episode, asscet, asscet_typ, _ = re.split(r'_|.ma', file_name)
            asscet = asscet.title()
            version_dict = assect_dict.get(asscet, [{0: ''}])[-1]
            print(assect_dict)
            print(asscet)
            version_int = list(version_dict.keys())[-1] + 1
            # 更新time_dict，将获得的资产放在对应集数下的list
            time_dict.setdefault(data, {episode:[]})
            # print(time_dict)
            # time_dict[data][episode].append(file_name)
            # 更新assect_dict，判断版本
            if version_int == 1:
                assect_dict[asscet] = [{version_int: {'time': data, 'episode': episode, 'asscet_typ': asscet_typ}}]
            else:
                assect_dict[asscet].append({version_int: {'time': data, 'episode': episode, 'asscet_typ': asscet_typ}})

            # 将资产复制到对应的项目目录中
            # 如果已经存在，则放入old_version并创建接收目录的文件夹
    # 将新的字典写入json中
    with open(asscet_json, 'w') as f:
        json.dump(assect_dict, f)
    with open(receive_json, 'w') as f:
        json.dump(time_dict, f)


if __name__ == '__main__':

    ipath = r'Z:\example\project\Inbox'
    log_path = r'Z:\log'
    receive_json = rf'{log_path}\receive_log.json'
    if os.path.exists(receive_json):
        os.remove(receive_json)
    asscet_json = rf'{log_path}\asscet_log.json'
    if os.path.exists(asscet_json):
        os.remove(asscet_json)
    data = os.listdir(ipath)
    for i in data:
        record_input_log(i, ipath, log_path)