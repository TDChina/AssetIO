# -*- coding: gbk -*-
# .@FileName:shot_num_list
# @Date....:2019-08-20  10:06
# ..:XingLian
# 打包所需资产

import os
import re
import time
import shutil
import _winreg
import json


a = '''
'''.split()

def get_desktop():
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return _winreg.QueryValueEx(key, "Desktop")[0]


asspath = {'chr': ['cfx', 'rig', 'srf', 'mod'], 'prp': ['rig', 'srf', 'mod'],
           'env': ['mod', 'srf'], 'veh': ['rig', 'srf', 'mod']}
fold = {'rig': 'rigging', 'srf': 'surface', 'mod': 'model'}
desk = get_desktop()


f = open(r'C:\Users\zhangying.BUXI\Desktop\version.json', 'w')
for asstyp in asspath:  # 依次遍历chr，prp等资产
    allname = os.listdir('I:\\bproject\\wts\\publish\\asset\\{}'.format(asstyp))
    ass_typ_dic = {}
    for name in allname:  # tohr
        name_verse = {}
        typDic = {}
        for loctyp in asspath[asstyp]:  # 依次遍历每个资产的环节
            verlist = []
            if loctyp == 'cfx':
                versepath = 'I:\\bproject\\wts\\publish\\asset\\{}\\{}\\{}'.format(asstyp, name, loctyp)
                #  versepath
                if os.path.exists(versepath):
                    verselist = os.listdir(versepath)
                    verselist_hair = []
                    verselist_cloth = []
                    verselist_cfx = []

                    for each in verselist:
                        findhair = re.findall('{}.cfx.hair.v\d{{3}}$'.format(name), each)
                        #  findhair
                        if findhair:
                            verselist_hair.append(findhair[0])
                        findcloth = re.findall('{}.cfx.cloth.v\d{{3}}$'.format(name), each)
                        if findcloth:
                            verselist_cloth.append(findcloth[0])
                    verselist_hair.sort(key=lambda x: x[-3:])
                    verselist_cloth.sort(key=lambda x: x[-3:])
                    if verselist_hair :
                        verselist_cfx.append(verselist_hair[-1])
                    if verselist_cloth:
                        verselist_cfx.append(verselist_cloth[-1])
                    if verselist_cfx:
                        verlist.append(verselist_cfx)

            else:
                versepath = 'I:\\bproject\\wts\\publish\\asset\\{0}\\{1}\\{2}'.format(asstyp, name, loctyp,
                                                                                      fold[loctyp])
                if os.path.exists(versepath):
                    verselist = os.listdir(versepath)
                    for each in verselist:
                        verlists = re.findall('{}.{}.{}.v\d{{3}}'.format(name, loctyp, fold[loctyp]), each)
                        if verlists:
                            verlist.append(verlists[0])

                    verlist.sort(key=lambda x: x[-3:])
            if verlist:
                typDic[loctyp] = verlist[-1]
            name_verse[name] = typDic
        ass_typ_dic[asstyp] = name_verse
        json.dump(ass_typ_dic,f,ensure_ascii=False)
        f.write('\n')