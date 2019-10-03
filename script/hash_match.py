# coding=utf-8
# 导入hashlib模块
import hashlib


def hashi_match(file_path, bytes=1024):
    # 创建一个md5算法对象
    md5_1 = hashlib.md5()
    with open(file_path, 'rb') as f:
        # 更新文本
        md5_1.update(f.read())
    #  获取这个文件的MD5值
    ret = md5_1.hexdigest()
    return ret
