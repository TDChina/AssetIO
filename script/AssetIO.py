# -*- coding: utf-8 -*-  


import os
import re
import time
import shutil
import pprint
import zipfile
from pathlib import Path


# ----------------------------------------------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------------------------------------------


def timestamp_to_date(timestamp):
    """Timestamp Translate Date Format

    :param timestamp: float, time.time()
    :return: str, 'year-month-day hour:minute:second'
    """

    timeStruct = time.localtime(timestamp)

    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_file_create_time(file_path):
    """Get File Create Time

    :param file_path: str, file path
    :return: str, 'year-month-day hour:minute:second'
    """
    t = os.path.getctime(file_path)

    return timestamp_to_date(t)


def get_file_size(file_path):
    """Get File Size

    :param file_path: str, file path
    :return: float, unit:MB
    """
    file_size = os.path.getsize(file_path)

    file_size = file_size / float(1024 * 1024)

    return round(file_size, 2)


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


def zip_files(dir_path, zip_file_path):
    """Zip Files

    :param dir_path: str, folder path
    :param zip_file_path: str, zip file path
    :return: None
    """

    zip = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)

    for path, dir_names, filenames in os.walk(dir_path):

        filter_path = path.replace(dir_path, '')

        for filename in filenames:

            zip.write(os.path.join(path, filename), os.path.join(filter_path, filename))

    zip.close()


# ----------------------------------------------------------------------------------------------------------------------
# Parameter Definition
# ----------------------------------------------------------------------------------------------------------------------


customer_file_root = r'E:\TD_Python\midterm\example\project'

project_file_root = r'E:\TD_Python\midterm\example'

project_name = 'JDC'

asset_types = ['Cha', 'Env', 'Prop']


# ----------------------------------------------------------------------------------------------------------------------
# Get Customer's All Files
# ----------------------------------------------------------------------------------------------------------------------


customer_all_file = []

for root, dirs, files in os.walk(customer_file_root):

    for file in files:

        file_full_path = os.path.join(root, file)

        if file_full_path:

            customer_all_file.append(file_full_path)


# ----------------------------------------------------------------------------------------------------------------------
# Get Assets Time
# ----------------------------------------------------------------------------------------------------------------------


get_assets_time = get_file_create_time(customer_file_root)


# ----------------------------------------------------------------------------------------------------------------------
# Files Mapping ：Customer
# ----------------------------------------------------------------------------------------------------------------------


mapping_data = []

for f in customer_all_file:

    file_path_obj = Path(f)

    result = {str(file_path_obj): {}}

    file_path_parts = file_path_obj.parts

    EP_Number = [p for p in file_path_parts if re.match(r'^EP\d+$', p)]

    file_name, file_format = file_path_obj.stem, file_path_obj.suffixes[0]

    file_asset_type = file_name.split('_')[-1]

    asset_Type = ''

    if file_asset_type in 'chaenvprop':

        asset_Type = file_asset_type.capitalize()

    asset_Name = file_path_obj.parent.name

    asset_File = file_path_obj.name

    for d, k in result.items():

        k['EP_Number'] = EP_Number[0]

        k['Asset_Type'] = asset_Type

        k['Asset_Name'] = asset_Name

        k['Asset_File'] = asset_File

    mapping_data.append(result)


# ----------------------------------------------------------------------------------------------------------------------
# Files Mapping ：Project
# ----------------------------------------------------------------------------------------------------------------------


project_file_root_folder_obj = Path(project_file_root)

project_file_root_obj = project_file_root_folder_obj / project_name

backups_count = 0

restore_data = {}

for customer_file_data in mapping_data:

    for f, data in  customer_file_data.items():

        file_asset_type = data['Asset_File'].split('.')[-1]

        project_file_rename = f"{project_name}_{data['Asset_Name']}_{data['Asset_Type']}.{file_asset_type}"

        project_file_path = project_file_root_obj / data['EP_Number'] / 'Asset' / data['Asset_Type'] \
                            / data['Asset_Name'] / project_file_rename

        if  not project_file_path.exists():

            project_file_parent_path = project_file_path.parent

            project_file_parent_path.mkdir(parents=True, exist_ok=True)

            data['Project_File_New_Path'] = str(project_file_path.absolute())

            shutil.copy2(f, data['Project_File_New_Path'])

        else:

            data['Project_File_New_Path'] = str(project_file_path.absolute())

            latest_file = get_latest_file(f, data['Project_File_New_Path'])

            if latest_file == f :

                if backups_count == 0:

                    time_val = time.time()

                    timestamp_to_date_str = timestamp_to_date(time_val)

                    backups_zip_name = f"{project_file_root_obj.name}_{timestamp_to_date_str}.zip".replace(':', '_')

                    backups_zip_path = project_file_root_folder_obj / backups_zip_name

                    zip_files(str(project_file_root_obj.resolve()), str(backups_zip_path.resolve()))

                    backups_count = 1

                shutil.copy2(f, data['Project_File_New_Path'])

                restore_data[f"{data['Project_File_New_Path']}"] = f


# ----------------------------------------------------------------------------------------------------------------------
# Restore
# ----------------------------------------------------------------------------------------------------------------------


restore_zip_count = 0

for p_path, c_path in  restore_data.items():

    shutil.copy2(p_path, c_path)

    if restore_zip_count == 0:

        time_val = time.time()

        timestamp_to_date_str = timestamp_to_date(time_val)

        restore_zip_name = f"{timestamp_to_date_str}.zip".replace(':', '_')

        zip_files(customer_file_root, f"{customer_file_root}/{restore_zip_name}" )


# ----------------------------------------------------------------------------------------------------------------------
# Print
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    print(f"Receive files's time is {get_assets_time}")

    print(f"Number of files is {len(customer_all_file)}")

    print(f"Receive files's are {customer_all_file}")

    pprint.pprint(mapping_data)

    pprint.pprint(restore_data)



