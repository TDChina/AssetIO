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


# 对源文件的路径进行处理，返回目标文件的路径，不对文件夹进行处理
def exec_filename(source_path, dec_path):
    file_path, filename = os.path.split(dec_path)
    filename_temp = file_path.split("/")
    new_name = file_path + "/" + filename_temp[-4] + "_" + filename_temp[-1].capitalize() + "_" +\
               filename_temp[-2].capitalize() + "." + filename.split(".")[-1]
    return new_name, source_path


def execfoder_filename(source_path, dec_path):
    shutil.copy(source_path, dec_path)
    new_name, source_path = exec_filename(source_path, dec_path)
    move_file(dec_path, new_name)
    return new_name, source_path


def exception(dec_folder):
    try:
        os.makedirs(dec_folder)
    except FileExistsError:
        pass


def traverfile_changename(_type, filepath, project_name, position, new_old_name_message, path, lable):
    for file in filepath[position]:
        dec_folder = os.path.split(path)[0] + "/" + project_name + "Asset/" + _type + "/" + \
                     str(file.split("_")[-2]).capitalize()
        if lable:
            exception(dec_folder)
            newname, oldname = execfoder_filename(file, dec_folder + "/" + file.split("/")[-1])
            new_old_name_message[newname] = oldname
        else:
            newname, oldname = exec_filename(file, dec_folder + "/" + file.split("/")[-1])
            new_old_name_message[newname] = oldname


# 返回一个新旧路径的字典 不创建文件夹
def create_new_old(assert_Type, filepath, project_name, path, lable=0):
    new_old_name_message = {}
    for _type in assert_Type:
        # 将文件放入存好的文件夹中
        if _type == "Pro":
            traverfile_changename(_type, filepath, project_name, 2, new_old_name_message, path, lable)

        elif _type == "Env":
            traverfile_changename(_type, filepath, project_name, 1, new_old_name_message, path, lable)

        elif _type == "Cha":
            traverfile_changename(_type, filepath, project_name, 0, new_old_name_message, path, lable)
    return new_old_name_message


# 返回一个新旧路径的字典 创建文件夹
def createfolder_newolddict(assert_Type, filepath, project_name, path):
    new_old_name = {}
    new_old_name = create_new_old(assert_Type, filepath, project_name, path, lable=1)
    print("the file struct has created!!!")
    return new_old_name


if __name__ == "__main__":
    source = 'D:/school/TdClass/AssetIO/example/project/Inbox/20191001/EP01/timer/EP01_Timer_pro.ma'
    dec = "D:/school/TdClass/AssetIO/example/project/TDC/Asset/Pro/Timer/EP01_Timer_pro.ma"
    a, b = exec_filename(source, dec)
    print("new: %s \nold: %s" % (a, b))