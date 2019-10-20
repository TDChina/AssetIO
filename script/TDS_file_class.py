# -*- coding: utf-8 -*-
# .@FileName:TDS_file_class
# @Date....:2019-10-17  23:43   
# ..:XingLian
"""
对象属性：接收路径，项目路径，log路径
对象方法：查看接收的文件，记录log，转存到项目路径，备份文件
"""
import json
import os
import re
import shutil

from script.find_file import get_files_list_fun


class FileOI:
    def __init__(self):
        self.input_path = r'Z:\example\project\Inbox'
        self.object_path = r'Z:\Project\TDC\Asset'
        self.log_path = r'Z:\log'

    def find_asscet(self, data):
        re_str = r'ep\d{2}_[a-z]+_(?:env|cha|pro)\.ma'
        file_list = [i for i in get_files_list_fun(rf'{self.input_path}\{data}') if re.search(re_str, i, re.I)]
        return file_list

    def filename_to_list(self, file_name):
        *_,  data, _, _, episode, asscet, asscet_typ, _ = re.split(r'/|_|(?:\.ma$)', file_name)
        asscet = 'Prop' if asscet == 'pro' else asscet.title()
        return data, episode, asscet, asscet_typ

    def creat_log(self, log_typ=1):
        if log_typ == 1:
            log_name = 'asscet'
        else:
            log_name = 'receive'
        log_json = rf'{self.log_path}\{log_name}_log.json'
        if os.path.exists(log_json):
            with open(log_json, 'r') as f:
               log_dict = json.load(f)
        else:
            f = open(log_json, 'w')
            f.close()
            asscet_dic = {'asscet_name': [{'time': '', 'episode': '', 'asscet_typ': ''}]}
            log_dic = {'time': {'episode': ['asscet_name']}}
            log_dict = asscet_dic if log_name == 'asscet' else log_dic
            with open(log_json, 'w') as f:
                json.dump(log_dict, f)
        return log_dict

    def creat_asscet_log(self,file_name):
        data, episode, asscet, asscet_typ = self.filename_to_list(file_name)
        log_json = rf'{self.log_path}\asscet_log.json'
        log_dict = self.creat_log()
        if not log_dict.get(asscet, False):
            log_dict[asscet] = [{'time': data, 'episode': episode, 'asscet_typ': asscet_typ}]
        else:
            log_dict[asscet].append({'time': data, 'episode': episode, 'asscet_typ': asscet_typ})
        with open(log_json, 'w') as f:
            json.dump(log_dict, f)

    def creat_time_log(self, file_name):
        data, episode, asscet, asscet_typ = self.filename_to_list(file_name)
        log_json = rf'{self.log_path}\receive_log.json'
        log_dict = self.creat_log(0)

        if not log_dict.get(data, False):
            log_dict[data] = {episode: [file_name.split('/')[-1]]}
        else:
            if not log_dict[data].get(episode, False):
                log_dict[data][episode] = [file_name.split('/')[-1]]
            else:
                log_dict[data][episode].append(file_name.split('/')[-1])
        with open(log_json, 'w') as f:
            json.dump(log_dict, f)

    def copy_file(self, file_name):
        data, episode, asscet, asscet_typ = self.filename_to_list(file_name)
        log_json = rf'{self.log_path}\asscet_log.json'
        with open(log_json, 'r') as f:
            log_dict = json.load(f)

        asscet_list = log_dict[asscet]
        if len(asscet_list) == 1:
            if not os.path.exists(rf'{self.object_path}\{asscet_typ}\{asscet}'):
                os.makedirs(rf'{self.object_path}\{asscet_typ}\{asscet}\backup')
            shutil.copyfile(file_name, rf'{self.object_path}\{asscet_typ}\{asscet}\{asscet}.ma')
        else:
            backup_file = asscet_list[-2]
            data_o, episode_o, asscet_typ_o = backup_file
            back_dir = rf'v{len(asscet_list)-2:0>3}_{data_o}'
            os.makedirs(rf'{self.object_path}\{asscet_typ}\{asscet}\backup\{back_dir}')
            os.rename(rf'{self.object_path}\{asscet_typ}\{asscet}\{asscet}.ma',
                      rf'{self.object_path}\{asscet_typ}\{asscet}\backup\{back_dir}\{episode_o}_{asscet}_{asscet_typ_o}.ma')
            shutil.copyfile(file_name, rf'{self.object_path}\{asscet_typ}\{asscet}\{asscet}.ma')


if __name__ == '__main__':
    foo = FileOI()
    foo.input_path = r'Z:\example\project\Inbox'
    foo.log_path = r'Z:\log'
    foo.object_path = r'Z:\Project\TDC\Asset'
    receive_json = rf'{foo.log_path}\receive_log.json'
    if os.path.exists(receive_json):
        os.remove(receive_json)
    asscet_json = rf'{foo.log_path}\asscet_log.json'
    if os.path.exists(asscet_json):
        os.remove(asscet_json)
    data = os.listdir(foo.input_path)
    for i in data:
        file_list = foo.find_asscet(i)
        print(rf'{i} 共接收了{len(file_list)}个文件')
        for file_name in file_list:
            print(file_name.split('/')[-1])
            foo.creat_asscet_log(file_name)
            foo.creat_time_log(file_name)
            foo. copy_file(file_name)
