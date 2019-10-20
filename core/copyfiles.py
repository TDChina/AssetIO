# -*- coding: utf-8 -*-
import re
import os
import shutil
import time
#-------获取所有文件的集数，场号，镜头号
def listdir(path):
    allPath = []
    allFiles = []
    for dirpath, dirnames, filenames in os.walk(path):
        #print('文件路径', dirpath)
        #print('文件夹名字', dirnames)
        allPath.append(dirpath)
        for filename in filenames:
            #print('文件名', filename)
            allFiles.append(filename)
    return (allPath,allFiles)

def setNewPath(original_path,target_path):#根绝原始文件目录创建新路径下的文件夹目录
    getpath = listdir(original_path)
    for i in getpath[0]:
        #print(i)
        target_name = i.replace(original_path,target_path)
        #print(target_name)
        if not os.path.exists(target_name):
            os.makedirs(target_name)
def creatfolder(target_path):#根据收到的maya文件名称创建集号，镜头号等..
    temp = getNum(original_path)
    ep = set(temp[0])
    sc = set(temp[1])
    cam = set(temp[2])
    for i in ep:
        temp_ep_path = os.path.join(target_path,i)
        #print(temp_ep_path)
        if not os.path.exists(temp_ep_path):
            #print(temp_ep_path)
            os.makedirs(temp_ep_path)
        for i in cam:
            temp_cam_path = os.path.join(temp_ep_path,i)
            if not os.path.exists(temp_cam_path):
                os.makedirs(temp_cam_path)

def getNum(original_path):#根据给到的maya文件名称获得集号镜头号等..
    allFiles = listdir(original_path)
    #print(allFiles[1])
    ep = []
    sc = []
    cam = []
    joinpath =[]
    '''allFiles = ["ep05_sc001_cam001_v001", "ep06_sc001_cam002a_v004", "ep06_sc003_cam001b_v002", "ep04_sc003_cam009H_v002",
            "ep06_sc004_cam001a-v001"]'''
    re_rule_pattern = re.compile(r'(ep\d{1,4}).*?(sc\d{1,4}).*?(cam\d{1,4}[a-z]*).*?(v\d{1,4})?', re.I)
    for i in allFiles[1]:
        num = re.findall(re_rule_pattern,i)
        #print(i)
        if num:
            ep.append(num[0][0])
            sc.append(num[0][1])
            cam.append(num[0][1]+"\\"+num[0][2])
            joinpath.append(num[0][0]+"\\"+num[0][1]+"\\"+num[0][2])
            #print(num[0][0])
    return(ep,sc,cam,joinpath)

def copyall(original_path, target_path):#原封不动的复制到目标路径下，不更改原有文件层级结构(备份所有原始文件)
    for files in os.listdir(original_path):
        base_name = os.path.join(original_path, files)
        target_name = os.path.join(target_path, files)
        if os.path.isfile(base_name):
            shutil.copy(base_name, target_name)
        else:
            if not os.path.isdir(target_name):
                os.makedirs(target_name)
            copyall(base_name, target_name)
def copy_files(original_path, target_path):#根据maya文件集数镜头号复制文件
    count = 0
    '''if not os.path.exists(target_path):
        os.makedirs(target_path)'''
    for f in os.listdir(original_path):
        base_name = os.path.join(original_path, f)
        if os.path.isfile(base_name):
            creatfolder(target_path)
            re_rule_pattern = re.compile(r'(ep\d{1,4}).*?(sc\d{1,4}).*?(cam\d{1,4}[a-z]*).*?(v\d{1,4})?', re.I)
            num = re.findall(re_rule_pattern, f)
            shotNum = num[0][0]+"\\"+num[0][1]+"\\"+num[0][2]
            #print("镜头名称 {} ".format(shotNum))
            count += 1
            #print("复制文件名是 {} 复制顺序是 {}".format(f, count))
            base_name = os.path.join(original_path, f)
            target_name = os.path.join(target_path + "\\" + shotNum, f)
            fileType = os.path.splitext(base_name)
            finalname = num[0][0]+"_"+num[0][1]+"_"+num[0][2]+ "_" +"final"
            #print("fianlName   {}".format(finalname))
            target_final_name = os.path.join(target_path + "\\" + shotNum, finalname) + fileType[1]
            #print("finalpathName   {}".format(target_final_name))
            #print("typw  {}".format(fileType))
            #print("原始路径文件 {} 目标路径文件 {}".format(base_name, target_name))
            #--------------------复制最新的文件并备份老文件添加版本号
            if os.path.isfile(base_name):
                #print("ok")
                if  os.path.isfile(target_final_name):
                    backupPath = os.path.join(target_path + "\\" + shotNum + "\\" + "backup")
                    #print("backup   {}".format(backupPath))
                    if not os.path.exists(backupPath):
                        os.makedirs(backupPath)
                    backupNum =  len([lists for lists in os.listdir(backupPath) if os.path.isfile(os.path.join(backupPath, lists))])+1
                    backupName =  num[0][0]+"_"+num[0][1]+"_"+num[0][2]+ "_" +  ("v%03d" % backupNum) + fileType[1]
                    #print("backupname  {} ".format(backupName))
                    backupfile = os.path.join(backupPath,backupName)
                    #print("backupnamepath  {} ".format(backupfile))
                    shutil.move(target_final_name,backupfile)
                    shutil.copy(base_name, target_name)
                    os.rename(target_name, target_final_name)
                else:
                    shutil.copy(base_name, target_name)
                    os.rename(target_name,target_final_name)
        else:#如果复制文件夹内有子文件夹，则把子目录文件复制到目标路径根目录下
             #print("子文件夹是 {} ".format(f))
             for root, dirs, files in os.walk(original_path):
                 for dir in dirs:
                     #print("dir  {}".format(dir))
                     oldsubfolder = os.path.join(root,dir)
                     #print("oldsubfolder   {}  ".format(oldsubfolder))
                     newsubfolder =oldsubfolder.replace(original_path,target_path)
                     #print("NEWsubfolder   {}  ".format(newsubfolder))
                     if not os.path.isdir(newsubfolder):
                        os.makedirs(newsubfolder)
                     copyall(oldsubfolder,newsubfolder)
def log_exist(log_path):#log是否存在,不存在则创建log
    filename = os.path.join(log_path, 'Projectinformation.txt')
    print("filename   {}".format(filename))
    if os.path.exists(filename):
        pass
    else:
        a = open(filename, 'w')
        a.close()

def add_log(original_path,target_path,projectpath):
    count = 0
    Projectinformation = os.path.join(projectpath, 'Projectinformation.txt')
    for root , dirs, files in os.walk(original_path):
        for name in files:
            count+=1
            temp_path = os.path.join(root,name)
            #print("temp_path  {}".format(temp_path) )
            file_name = temp_path.replace(original_path, target_path)
            #print("file_name  {}".format(file_name))
            file_time = os.stat(temp_path).st_mtime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time))
            #print("file time  {}".format(file_modify_time))
            with open(Projectinformation,'a') as f:
                f.write( ','.join( ['%d'%count,"原始文件路径及修改时间",'%s' % temp_path , '%s\n' % file_modify_time] ) )
                f.close()

#----
if __name__ == '__main__':
    original_path = r"D:\myFn\TD_class\test_file\Ani"
    target_path = r"D:\myFn\TD_class\test_file\target\Ani"
    log_path = r"D:\myFn\TD_class\test_file\target"
    #copyall(original_path, target_path)
    copy_files(original_path,target_path)
    add_log(original_path, target_path, log_path)

