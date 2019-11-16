import os
import time
import shutil
import zlib
import json

class Inbox:		
	
	
	def __init__(self,dir=r'H:\git\AssetIO-master\example\project\Inbox')   
	#Customer file path
	self.dir = dir
	self.cust = os.path.basename(dir)
	os.chdir(self.dir)		
	self.input_data ={}
	
	
	def get_input_data(self):
		#get the original name and path of the file,also to get the file type and name
		# root 所指的是当前正在遍历的这个文件夹的本身的地址
		# dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
		# files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
		for root, dirs, files in os.walk('.'):
			if files[0].endswith('.ma'):
				self.epnum, self.obj, self.form = os.path.splitext(i)[0].split('_')   
				self.file_data = {
					'input_file_name': files[0]
					'input_file_path': os.path.abspath(root)
					'output_file_epname': self.epnum.title()
					'output_file_obj': self.obj.title()
					'output_file_form': self.form.title()
				}
				self.input_data[files[0]] = self.file_data
		return 	self.input_data	
		
	
	def get_input_info(self):	
		#get time
		self.time_info = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(os.path.getctime('.')))    
		#form get_input_data get file_name
		self.file_name = self.get_input_data().keys()
		#count numbers of the file
		self.file_len = len(self.file_name)
		#self.input_info = 'Time:{}\nCount:{}\nContent:\n{}'.format(self.time_info,self.file_len,'\n'.join(self.file_name))
		self.input_info = {time:self.time_info,len:self.file_len,name:self.file_name}
		return self.input_info
		
	
	def create_directory(self,directory):
		if not os.path.isdir(directory):
			os.makedirs(directory)
		
		
	def set_project_path(self,path='H:\git\AssetIO-master\example\project\TDC'):
		#set project path(default:'H:\git\AssetIO-master\example\project\TDC')
		return path 
	

	def publish_input_files(self):
		#get local_path and project_name
		self.project_path = self.set_project_path()
		self.project_name = self.project_path.rpartition('\\')[-1]
		#from get_input_data get data
		for file in self.get_input_data():		
			#data_format to get dictionary values and keys
			self.asset_name = f'{self.project_name}_{file[output_file_obj]}_{file[output_file_form]}.ma'
			self.old_file = f'{os.path.abspath(file[input_file_path])}{os.sep}{file[input_file_name]}.ma'
			self.new_path = os.path.join(self.project_path, 'Asset', file[output_file_form], file[output_file_obj])
			self.new_file = os.path.join(self.new_path,self.asset_name)
			#check path rationality
			self.create_directory(self.new_path)
			#copy to new folder
			shutil.copy(self.old_file,self.new_file)
		
		
	def date_file_info(self,projet_name='TDC_info', directory="H:\git\AssetIO-master\example\project"):
		# save json file
		self.save_file = f'{directory}{os.sep}{projet_name}.json'
		with open(self.save_file, 'w+') as f:
			json.dump(get_input_info,f)
	
	
	def file_backups(self,source_directory = r'H:\git\AssetIO-master\example\project\TDC',target_directory = r'H:\git\AssetIO-master\example\project'):
		self.source_directory = source_directory
		self.target_backups = target_directory
		#backups muti-folder
		if not os.path.isdir(self.target_backups):
		#determine if the first backup is made判断是否第一次备份
			f'{os.path.basename(self.source_directory)}_000'
		else:
		#Otherwise look for the last bit of the folder否则寻找文件夹最后一位
			for floder in os.listdir(self.target_backups):
				#increase the version number if the folder is the project and the latest file exists如果文件夹是该项目并且存在最新档则增加版本号
				if os.path.isdir(self.target_backups) and os.path.basename(self.source_directory) in floder:
					self._num = str(int(floder.rpartition('_')[-1]) + 1)
		#the folder name is the project name and the 00 version number文件夹名称为项目名称和00版本号
		self.backups_name = f'{os.path.basename(self.source_directory)}_{self._num.zfill(3)}'
		self.backups_path = os.join(self.target_backups,self.backups_name)
		#check path rationality
		self.create_directory(self.backups_path)
		#init dir path
		shutil.copytree(self.source_directory, self.target_backups)
				
	
	
	def update_file(self,source_directory = r'H:\git\AssetIO-master\example\project\TDC',target_directory = r'H:\git\AssetIO-master\example\project'):
		#backups old file and overwrite new file 
		self.file_backups(source_directory,target_directory)
		self.publish_input_files()
	
	
	def submit_file(self, directory=r'H:\git\AssetIO-master\example\project\Inbox'):
		#get local_path and project_name
		self.project_path = self.set_project_path(path='')
		self.project_name = self.project_path.rpartition('\\')[-1]
		self.origin_info = self.get_input_data()
		self.submit_directory = directory
		os.chdir(directory)
		for file in self.get_input_data():		
			#data_format to get dictionary values and keys
			self.asset_name = f'{self.origin_info[file][output_file_epname]}_{self.origin_info[file][output_file_obj]}_{self.origin_info[file][output_file_form]}.ma'
			self.old_file = f'{os.path.abspath(file[input_file_path])}{os.sep}{file[input_file_name]}.ma'
			self.pulishtime = time.strftime('%Y%m%d',time.localtime(time.time()))
			self.new_path = os.path.join(self.submit_directory,self.pulishtime, self.origin_info[file][output_file_epname], file[output_file_obj])
			self.new_file = os.path.join(self.new_path,self.asset_name)
			#check path rationality
			self.create_directory(self.new_path)
			#copy to new folder
			shutil.copy(self.old_file,self.new_file)
		#zip and remove folder
		self.zip_path = os.path.join(self.submit_directory,self.pulishtime)
		self.zip_name = f'Inbox_{time.strftime('%Y%m%d',time.localtime(time.time()))}'
		self.zip_file(source_name = self.zip_name,source_directory = self.zip_path)
		shutil.rmtree(self.zip_path, ignore_errors=True)
	
	
	def zip_file(self,source_name = 'Inbox',source_directory= r'H:\git\AssetIO-master\example\project\Inbox'):
		shutil.make_archive(source_name, 'zip', source_directory)
		
	

