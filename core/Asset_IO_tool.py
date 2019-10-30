# coding=utf-8
import os
import pprint
import shutil
import time
import json


def get_input_data():
    input_dir = input("请选择客户文件路径>>>>>>>>>>")
    # r'C:\Users\geyij\Desktop\new\AssetIO\example\project\Inbox\20191001'
    input_data = {}
    for a, b, c in os.walk(input_dir):
        if c:
            if c[0].endswith('.ma'):
                i, j, k = c[0].split('.')[0].split('_')
                file_info = {
                    'input_file_name': c[0],
                    'input_file_path': a,
                    'asset_name': j.lower(),
                    'asset_type': k.lower(),
                    'seq': i.upper()
                }
                input_data[file_info['asset_name']] = file_info
    return input_data, input_dir


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_time(directory):
    file_time_sec = os.path.getctime(directory)
    file_time_struct = time.localtime(file_time_sec)
    file_time_str = time.strftime('%Y-%m-%d-%H-%M-%S', file_time_struct)
    return file_time_str


def bak_file(directory):
    file_directory = directory
    file_path = os.path.split(file_directory)[0]
    file_name = os.path.split(file_directory)[1]
    file_time = get_file_time(file_directory)
    bak_path = os.path.join(file_path, 'bak', file_time)
    create_directory(bak_path)
    bak_name = os.path.splitext(file_name)[0] + '_' + file_time + os.path.splitext(file_name)[1]
    bak_file_directory = os.path.join(bak_path, bak_name)
    os.rename(file_directory, bak_file_directory)


def save_data_file(data, name, directory):
    save_data = data
    save_name = name + '.json'
    save_path = directory
    save_file = os.path.join(save_path, save_name)
    with open(save_file, 'w+') as f:
        json.dump(save_data, f)
    return save_file


def copy_input_files():
    assets_data, input_dir = get_input_data()
    show_dir = input("请选择项目路径>>>>>>>>>>>")
    # r'C:\Users\geyij\Desktop\new\AssetIO\example\project\TDC'
    show_name = show_dir.rpartition('\\')[-1]

    input_dir_time = get_file_time(input_dir)
    data_file_name = 'Input_Data_' + input_dir_time

    for asset, info in assets_data.items():
        asset_name = info['asset_name'].capitalize()
        asset_type = info['asset_type'].capitalize()
        save_name = f'{show_name}_{asset_name}_{asset_type}.ma'
        save_path = os.path.join(show_dir, 'Asset', asset_type, asset_name)
        save_file = os.path.join(save_path, save_name)
        create_directory(save_path)
        if os.path.exists(save_file):
            bak_file(save_file)
        input_file = os.path.join(assets_data[asset]['input_file_path'], assets_data[asset]['input_file_name'])
        shutil.copy(input_file, save_file)
        assets_data[asset]['saved_file_name'] = save_name
        assets_data[asset]['saved_file_path'] = save_path

    saved_data_file = save_data_file(assets_data, data_file_name, input_dir)

    return assets_data, saved_data_file


output_assets_str = 'victor'
print(output_assets_str)

