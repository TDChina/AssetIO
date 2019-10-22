# -*- coding: UTF-8 -*-

import os
import re
import yaml
import shutil
import pprint


def record_original_file(asset_path, output_path):
    """记录原始资产的文件结构，和文件修改时间等文件信息,并输出yml文件

    Args:
        asset_path:需要记录资产的路径
        output_path:yml文件的输出路径

    Returns:
        (记录文件信息的yml文件路径, 记录文件路径的yml文件路径)
    """
    # 设置工作目录
    os.chdir(asset_path)
    # {文件名：文件信息}
    original_file_info_dict = {}
    # {文件名：文件所在路径}
    original_asset_path_dict = {}
    # 获取原始文件路径
    for root, dirs, file_list in os.walk('.'):
        if file_list:
            for file_name in file_list:
                full_path = os.path.join(root, file_name)
                original_file_info_dict[file_name] = os.stat(full_path)
                # 存储工作目录和相对路径
                original_asset_path_dict[file_name] = [asset_path, os.path.join(root[2:], file_name)]
    # 输出文件信息
    file_info_path = os.path.join(output_path, f'{project_code}_file_information.yml')
    with open(file_info_path, 'w') as file_info:
        yaml.dump(original_file_info_dict, file_info)
    # 输出文件路径
    file_path_path = os.path.join(output_path, f'{project_code}_file_path.yml')
    with open(file_path_path, 'w') as file_info:
        yaml.dump(original_asset_path_dict, file_info)
    return file_info_path, file_path_path


def transfer_asset(target_path, backup_in_path, backup_out_path):
    """转移资产并记录文件的原始名字和修改后的名字

    Args:
        target_path:原始文件路径
        backup_in_path:记录文件路径的yml文件路径
        backup_out_path:输出新旧文件名的yml文件路径

    Returns:
        记录新旧文件名的yml文件路径
    """
    # 设置工作路径
    os.makedirs(target_path, exist_ok=True)
    os.chdir(target_path)
    # 读取bake文件，提取所有文件名
    with open(backup_in_path) as file_path_info:
        file_path_dict = yaml.load(file_path_info, Loader=yaml.FullLoader)
    file_name_list = list(file_path_dict.keys())
    # 解析旧文件名，得到新文件名,并复制到对应路径
    # {旧文件：新文件名}
    new_old_name_dict = {}
    for file_old_name in file_name_list:
        # 匹配出镜头号，资产名，资产类型
        result = (re.match(r'([e|E][p|P]\d{2})_([a-z|A-Z]+)_(pro|cha|env)', file_old_name))
        shot_name, asset_name, asset_type = result.group(1, 2, 3)
        asset_name = asset_name.capitalize()
        new_name = f'{project_code}_{asset_name}_{asset_type}.ma'
        new_old_name_dict[new_name] = file_old_name
        old_path = os.path.join(file_path_dict[file_old_name][0], file_path_dict[file_old_name][1])
        asset_path = os.path.join(target_path, 'Asset')
        # 文件分类
        if asset_type == 'pro':
            new_path = os.path.join(asset_path, 'Prop', new_name)
        elif asset_type == 'cha':
            new_path = os.path.join(asset_path, 'Cha', new_name)
        elif asset_type == 'env':
            new_path = os.path.join(asset_path, 'Env', new_name)
        else:
            print('-' * 10, 'Meet an unknown type of --->', asset_type)
        # 复制文件
        os.makedirs(os.path.splitext(new_path)[0], exist_ok=True)
        shutil.copy(old_path, new_path)
    # 输出新旧名字的bake文件
    name_bake_path = os.path.join(backup_out_path, f'{project_code}_new_old.yml')
    with open(name_bake_path, 'w') as name_history:
        yaml.dump(new_old_name_dict, name_history)
    return name_bake_path


def return_file_and_packing(source_path, target_path, backup_name_path, backup_path_path):
    """对文件打包，并还原原始文件命名和文件结构

    Args:
        source_path: 需要打包的文件根目录
        target_path: 存放打包好的文件的地址
        backup_name_path: 存放记录旧文件命名的yml文件路径
        backup_path_path: 存放记录旧文件路径的yml文件路径

    Returns:

    """
    # 设置工作目录
    os.makedirs(target_path, exist_ok=True)
    os.chdir(target_path)
    # 从yml文件中解析出文件的旧名字
    with open(backup_name_path) as file_name:
        file_name_dict = yaml.load(file_name, Loader=yaml.FullLoader)
    # 从yml文件中解析出文件的旧路径
    with open(backup_path_path) as file_path:
        file_path_dict = yaml.load(file_path, Loader=yaml.FullLoader)
    # 修改文件名并复制
    for root, dirs, file_list in os.walk(source_path):
        if file_list:
            for file_name in file_list:
                original_name = file_name_dict[file_name]
                file_path = file_path_dict[original_name][1]
                file_new_path = os.path.abspath(os.path.join(file_path))
                current_path = os.path.join(root, file_name)
                os.makedirs(os.path.splitext(file_new_path)[0], exist_ok=True)
                shutil.copy(current_path, file_new_path)


if __name__ == '__main__':
    project_code = 'TDC'
    project_path = r'D:\code\MyItem\td_study\mid_term_work\AssetIO\example\project'
    target_path = os.path.join(project_path, project_code)
    original_asset_path_dict = os.path.join(project_path, 'Inbox')
    packing_path = os.path.join(project_path, 'package')
    # 首先记录文件信息
    file_info_path, file_path_path = record_original_file(asset_path=original_asset_path_dict, output_path=project_path)
    # 转移文件
    backup_name_path = transfer_asset(target_path=target_path, backup_in_path=file_path_path,
                                      backup_out_path=project_path)
    # 还原文件结构
    return_file_and_packing(source_path=target_path, target_path=packing_path, backup_name_path=backup_name_path,
                            backup_path_path=file_path_path)
