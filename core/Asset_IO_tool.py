# coding=utf-8
import os
asset_types = {'pro': 'Pro',
               'cha': 'Cha',
               'env': 'Env'}
asset_names = {}
input_dir = r'C:\Users\geyij\Desktop\new\AssetIO\example\project\Inbox\20191001'
# TODO 改成input"请选择客户文件路径>>>>>>>>>>"
show_dir = r'C:\Users\geyij\Desktop\new\AssetIO\example\project\TDC'
# TODO 改成input "请选择项目路径>>>>>>>>>>>"
show_name = show_dir.rpartition('\\')[-1]

for a, b, c in os.walk(input_dir):
    if c[0].endswith('.ma'):
        print(a)
        print(b)
        print(c)

