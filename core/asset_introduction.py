# -*- coding: UTF-8 -*-
"""
@File    : asset_introduction.py
@Vision  : 1.0.0
@Time    : 2019/10/3 17:34
@Author  : Qing Shuang
@Email   : 2075693226@qq.com
@Software: PyCharm
"""

import os
import re
import time
import pickle
import shutil
import pprint


def record_original_file(asset_path, output_path):
    """记录原始资产的文件结构，和文件修改时间"""
    original_file_structure = {}
    file_info = {}
    # 获取原始文件结构
    for root, dirs, files in os.walk(asset_path):
        if root == asset_path:
            original_file_structure['Inbox'] = dirs + files
        else:
            dict_key = root.split('\\')[-1]
            original_file_structure[dict_key] = dirs + files
        if len(files) > 0:
            for file in files:
                file_path = f'{root}\\{file}'
                file_modify_time = time.ctime(os.path.getmtime(file_path))
                file_info[file] = [file_path, file_modify_time]
    # 指定bake文件的路径
    # backup_data_path = output_path + '\\' + project_code + '.bake'
    all_info_list = [original_file_structure, file_info]
    backup_data_path = f'{output_path}\\{project_code}.bake'
    # 输出bake文件
    with open(backup_data_path, 'wb') as file_structure:
        pickle.dump(all_info_list, file_structure)


def transfer_asset(target_path, bake_path):
    """转移资产并记录文件的原始名字和修改后的名字"""
    # 创建必需的文件夹结构
    filter_path = target_path
    for filter_name in ['Project', project_code, 'Asset', ['Cha', 'Env', 'Prop']]:
        if isinstance(filter_name, str):
            filter_path = f'{filter_path}\\{filter_name}'
            if not os.path.exists(filter_path):
                os.makedirs(filter_path)
        else:
            for filter in filter_name:
                child_path = f'{filter_path}\\{filter}'
                if not os.path.exists(child_path):
                    os.makedirs(child_path)
    # 读取bake文件，提取所有文件名
    with open(bake_path, 'rb') as file_structure:
        all_info_list = pickle.load(file_structure)
    file_info_dict = all_info_list[1]
    file_name_list = list(file_info_dict.keys())
    # 解析旧文件名，得到新文件名,并复制到对应路径
    old_new_name_dict = {}
    for file in file_name_list:
        result = (re.match(r'([e|E][p|P]\d{2})_([a-z|A-Z]+)_(pro|cha|env)', file))
        shot_name, asset_name, asset_type = result.group(1, 2, 3)
        asset_name = asset_name.capitalize()
        new_name = f'{project_code}_{asset_name}_{asset_type}.ma'
        old_new_name_dict[file] = new_name
        old_path = file_info_dict[file][0]
        asset_path = target_path + r'\Project\TDC\Asset'
        # 文件分类
        if asset_type == 'pro':
            new_path = f'{asset_path}\\Prop\\{new_name}'
        elif asset_type == 'cha':
            new_path = f'{asset_path}\\Cha\\{new_name}'
        elif asset_type == 'env':
            new_path = f'{asset_path}\\Env\\{new_name}'
        else:
            print('-' * 10, 'Meet an unknown type of --->', asset_type)
        # 复制文件
        shutil.copy(old_path, new_path)
    # 输出新旧名字的bake文件
    name_bake_path = f'{target_path}\\{project_code}_name.bake'
    with open(name_bake_path, 'wb') as name_history:
        pickle.dump(old_new_name_dict, name_history)


if __name__ == '__main__':
    project_code = 'TDC'
    original_asset_path = r'C:\Users\qingshuang\Documents\code\MyItem\td_study\mid_term_work\AssetIO\example\project\Inbox'
    project_path = r'C:\Users\qingshuang\Documents\code\MyItem\td_study\mid_term_work\AssetIO\example\project'
    target_path = r'C:\Users\qingshuang\Documents\code\MyItem\td_study\mid_term_work\AssetIO\example\project\TDC'
    bake_path = r'C:\Users\qingshuang\Documents\code\MyItem\td_study\mid_term_work\AssetIO\example\project\TDC.bake'
    record_original_file(asset_path=original_asset_path, output_path=project_path)
    transfer_asset(target_path=target_path, bake_path=bake_path)
