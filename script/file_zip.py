# coding: gbk
import os
import winreg

# ��winrar���뻷������
oldenv = os.getenv('path')
os.environ['path'] = '{};Z:\Program Files\WinRAR'.format(oldenv)


# ��ȡ����·��
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


# ѹ���ļ�
def zip_file(opath, filename, *ipath):
    rar_command = "WinRAR a {0} {1}".format(r'{}\{}.rar'.format(opath, filename), *ipath)
    print(rar_command)
    if os.system(rar_command) == 0:
        print("{} rar �ɹ�".format(filename))
    else:
        print("{} rar ʧ��".format(filename))




