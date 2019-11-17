# coding = utf-8
# 导入要用的模块
import os
import shutil
import re

# 定义变量

My_Asset_type = ["Char", "Envir", "Prop"]
OUTSOURCE_DIR = r"Z:\project\TDC\Assets"
TARGET_DIR = r"X:\Mulan_Projects\Assets"
my_pattern = re.compile(r'EP\d[2]_\w_cha|env|pro.ma')


def list_ma_files(dirs):
    """

    Args:
        dir:

    Returns:list - ["Z:\project\TDC\Asset\My_Asset_type\xxxxx.ma",...]

    """
    all_ma_files = []
    for root, path, files in os.walk(dirs):
        for file_name in files:
            if os.path.splitext(file_name)[-1] == ".ma":
                all_ma_files.append(os.path.join(root, file_name))
    return all_ma_files


def match_file(all_ma_files):
    """

    Args:
        all_ma_files: list -

    Returns:

    """
    # 把文件名按照公司内部命名规范进行改名
    # 如果路径存在，则os.renames改名；不存在，则os.makedirs创建路径,并执行复制文件
    new_files = []
    for file_path in all_ma_files:
        old_name = os.path.basename(file_path)

        # 正则匹配

        if re.match(my_pattern, old_name):
            # 如果匹配成功,符合规范
            new_files.append(file_path)  # file_path 文件全路径
        else:
            new_name = "X:\Mulan_Projects\Assets\Char\cha|env|pro.ma"  # 全路径
            os.renames(file_path, new_name)
            new_files.append(new_path)
    return new_files


def copy_files(files):
    """

    Args:
        files: list

    Returns:

    """
    for correct_file in files:
        target_file = os.path.join(target_dir, os.path.basename(correct_file))
        shutil.copytree(correct_file, target_file)


if __name__ == '__main__':
    ma_files = list_ma_files(outsourse_dir)  # 找到所有maya文件
    correct_files = match_file(ma_files)  # 匹配所有maya文件，并重命名
    copy_files(correct_files)  # 复制文件
