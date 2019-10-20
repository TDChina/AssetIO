# coding: gbk
import os
import winreg

# 将winrar加入环境变量
oldenv = os.getenv('path')
os.environ['path'] = '{};Z:\Program Files\WinRAR'.format(oldenv)


# 获取桌面路径
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


# 压缩文件
def zip_file(opath, filename, *ipath):
    rar_command = "WinRAR a {0} {1}".format(r'{}\{}.rar'.format(opath, filename), *ipath)
    print(rar_command)
    if os.system(rar_command) == 0:
        print("{} rar 成功".format(filename))
    else:
        print("{} rar 失败".format(filename))




