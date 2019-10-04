# coding=utf-8
import shutil
import os
"""
将传入的源文件复制进入目标文件中，
将文件名首字母大写，并将其保存为格式{项目代号}{资产名}{资产类别}.ma
并返回一个字典，键为更改后的名字，值为更改前的名字
"D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/EP01_Timer_pro.ma"
"""


# 创建字典，定义函数进行文件复制
def move_file(dec_path, new_name):
    shutil.move(dec_path, new_name)


def exec_filename(source_path, dec_path):
    file_path, filename = os.path.split(dec_path)
    filename_temp = file_path.split("/")
    new_name = file_path + "/" + filename_temp[-4] + "_" + filename_temp[-1].capitalize() + "_" +\
               filename_temp[-2].capitalize() + "." + filename.split(".")[-1]
    return new_name, source_path


def execfoder_filename(source_path, dec_path):
    shutil.copy(source_path, dec_path)
    file_path, filename = os.path.split(dec_path)
    filename_temp = file_path.split("/")
    new_name = file_path + "/" + filename_temp[-4] + "_" + filename_temp[-1].capitalize() + "_" +\
               filename_temp[-2].capitalize() + "." + filename.split(".")[-1]
    move_file(dec_path, new_name)
    return new_name, source_path


# 返回一个新旧路径的字典 不创建文件夹
def create_new_old(assert_Type, filepath, project_name):
    new_old_name_message = {}
    for _type in assert_Type:
        # 将文件放入存好的文件夹中
        if _type == "Pro":
            for file in filepath[2]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                newname, oldname = exec_filename(file, dec_folder + "/" + file.split("/")[-1])
                new_old_name_message[newname] = oldname

        elif _type == "Env":
            for file in filepath[1]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                newname, oldname = exec_filename(file, dec_folder + "/" + file.split("/")[-1])
                new_old_name_message[newname] = oldname

        elif _type == "Cha":
            for file in filepath[0]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                newname, oldname = exec_filename(file, dec_folder + "/" + file.split("/")[-1])
                new_old_name_message[newname] = oldname
    # print("new_old_name_message", new_old_name_message)
    return new_old_name_message


# 返回一个新旧路径的字典 创建文件夹
def createfolder_newolddict(assert_Type, filepath, project_name):
    new_old_name = {}
    for _type in assert_Type:
        # 将文件放入存好的文件夹中
        if _type == "Pro":
            for file in filepath[2]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                try:
                    os.makedirs(dec_folder)
                except FileExistsError:
                    pass
                finally:
                    newname, oldname = execfoder_filename(file, dec_folder + "/" + file.split("/")[-1])
                    new_old_name[newname] = oldname

        elif _type == "Env":
            for file in filepath[1]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                os.makedirs(dec_folder)
                newname, oldname = execfoder_filename(file, dec_folder + "/" + file.split("/")[-1])
                new_old_name[newname] = oldname

        elif _type == "Cha":
            for file in filepath[0]:
                dec_folder = "D:/school/TdClass/AssetIO/example/project/" + project_name + "Asset/" + _type + "/" + \
                             str(file.split("_")[-2]).capitalize()
                os.makedirs(dec_folder)
                newname, oldname = execfoder_filename(file, dec_folder + "/" + file.split("/")[-1])
                new_old_name[newname] = oldname

    else:
        print("the file struct has created!!!")
        return new_old_name


if __name__ == "__main__":
    source = 'D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.ma'
    dec = "D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/EP01_Timer_pro.ma"
    a, b = exec_filename(source, dec)
    print("new: %s \nold: %s" % (a, b))