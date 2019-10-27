# -*- coding: utf-8 -*-  

import time
import datetime
import os


# 1.'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def timestamp_to_date(timestamp):
    """Timestamp Translate Date Format

    :param timestamp: float, time.time()
    :return: str, 'year-month-day hour:minute:second'
    """

    timeStruct = time.localtime(timestamp)

    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

time_val = time.time() # return 1570364955.402527
TimeStampToTime_val = timestamp_to_date(time_val) # return 2019-10-06 20:29:52
today = datetime.date.today() # return 2019-10-06
now = datetime.datetime.now() # return 2019-10-06 20:29:52.571413


# 2.'''获取文件的大小,结果保留两位小数，单位为MB'''
file1_path = r'E:\TD_Python\midterm\example\project\TDC\Asset\Cha\Victor\TDC_Victor_Cha2.ma'
file2_path = r'E:\TD_Python\midterm\example\project\TDC\Asset\Cha\Victor\TDC_Victor_Cha.ma'
def get_file_size(file_path):
    """Get File Size

    :param file_path: str, file path
    :return: float, unit:MB
    """
    file_size = os.path.getsize(file_path)

    file_size = file_size / float(1024 * 1024)

    return round(file_size, 2)

file_size = get_file_size(file1_path) #return 0.0


# 3'''获取文件的访问时间'''

def get_file_access_time(file_path):
    """Get File Assess Time

    :param file_path: str, file path
    :return: str, 'year-month-day hour:minute:second'
    """
    t = os.path.getatime(file_path)

    return timestamp_to_date(t)

get_file_access_time_val = get_file_access_time(file1_path)  # return 2019-10-02 12:53:02
print(get_file_access_time_val)


# 4'''获取文件的创建时间'''

def get_file_create_time(file_path):
    """Get File Create Time

    :param file_path: str, file path
    :return: str, 'year-month-day hour:minute:second'
    """
    t = os.path.getctime(file_path)
    return timestamp_to_date(t)

get_file_create_time_val = get_file_create_time(file1_path) # return 2019-10-02 12:53:02
print(get_file_create_time_val)

# 5'''获取文件的修改时间'''

def get_file_modify_time(file_path):
    """Get File Modify Time

    :param file_path: str, file path
    :return: str, 'year-month-day hour:minute:second'
    """
    t = os.path.getmtime(file_path)
    return timestamp_to_date(t)

get_file_modify_time_val = get_file_modify_time(file1_path) # return 2019-10-02 12:53:02
print(get_file_modify_time_val)

def get_latest_file(file1_path, file2_path):
    """Get The Latest File

    :param file1_path: str, file path
    :param file2_path: str, file path
    :return: str, file path
    """
    file1_time = os.path.getmtime(file1_path)
    file2_time = os.path.getmtime(file2_path)

    if file1_time > file2_time:

        return file1_path

    elif file1_time < file2_time:

        return file2_path

    else:

        return file1_path

latest_file = get_latest_file(file1_path,file2_path)
print(latest_file)



import os
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            print(os.path.join(root, file))
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件

root_files = file_name(r'E:\TD_Python\midterm\example')
print(root_files)


# ----------------------------------------------------------------------------------------------------------------------
# Doc
# ----------------------------------------------------------------------------------------------------------------------


# https://docs.python.org/3/library/pathlib.html
# https://zhuanlan.zhihu.com/p/56909212
