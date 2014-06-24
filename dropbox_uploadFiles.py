#!/usr/bin/python
# -*- coding: utf-8 -*- 
from dropbox import client, session 
import os 
import sys
import argparse
import pprint
import json
import re

APP_KEY = ""
APP_SECRET = ""
ACCESS_TOKEN = ''

parser = argparse.ArgumentParser(description = 'Python DropBox UploadDIR ver 0.1')
parser.add_argument('-s','--sourceDir', help=  u'Исходная директория', required = True, dest = 'sourcePath')
parser.add_argument('-t','--targetDir', help = u'Директория в DROPBOX', required = True, dest = 'targetPath')
parser.add_argument('-i1','--ignoreDirs', help = u'Названия локальных директорий, которые не нужны копировать. Разделяются - "|". Пример: cache|.git|svn', required = False, dest = 'ignoreDirs', default = False)
parser.add_argument('-i2','--ignoreFiles', help = u'Названия локальных файлов, которые не нужны копировать. Разделяются - "|". Пример: db.cfg|cache.bin|config.inc', required = False, dest = 'ignoreFiles', default = False)
parser.add_argument('-i3','--ignoreExt', help = u'Расширения локальных файлов, которые не нужны копировать. Разделяются - "|". Пример: .bin|.cache|.ini', required = False, dest = 'ignoreExt', default = False)
args = vars(parser.parse_args())

print "\n------------------------------------------------------------"

class DropBoxUpload():

	api_client = None
	path = '/'
	
	count_find_files = 0
	count_transfer_files = 0;
	count_ignore_files = 0;
	count_find_dirs = 0;
	count_ignore_dirs = 0;
	count_create_dirs = 0;
	
	def __init__(self, app_key, app_secret, access_token, args):
		
		self.api_client = client.DropboxClient(access_token)

		self.ignoreDirs = args['ignoreDirs'].split('|') if args['ignoreDirs'] is not False else []
		self.ignoreFiles = args['ignoreFiles'].split('|') if args['ignoreFiles'] is not False else []
		self.ignoreExt = args['ignoreExt'].split('|') if args['ignoreExt'] is not False else []
		
		self.sourcePath = args['sourcePath']
		self.targetPath = self.path + ('' if args['targetPath'] == '/' else args['targetPath'])
		
		self.sourcePath = self.sourcePath.replace('//', '/')
		self.targetPath = self.targetPath.replace('//', '/')
		
		print u"DROPBOX: Авторизация: успешна!";
		
		if not self.checkDir(self.targetPath):
			if not self.createDir(self.targetPath):
				self.cryExit();

		print u"DROPBOX: Директория '%s' доступна!" % self.targetPath
		print u"LOCAL: Начинаем рекурсивный проход по директории '%s'" % self.sourcePath
		
		ignoreDirsRegExp = '/' . join(self.ignoreDirs)
		ignoreDirsRegExp = '/' + ignoreDirsRegExp + ''
		
		_ignorDirs = []
		_files = [];
		
		for dir, subdirs, files in os.walk(self.sourcePath):
					
			self.count_find_dirs += 1
			
			c_dir = dir.replace(self.sourcePath, '')
			m_dir = os.path.basename(os.path.normpath(dir))

			if len(_ignorDirs) is not 0 and bool(re.search('^(' + '|' . join(_ignorDirs) + ')', c_dir)):
				continue
				
			elif len(self.ignoreDirs) is not 0 and (m_dir in self.ignoreDirs or bool(re.search(ignoreDirsRegExp, c_dir))):
			
					_ignorDirs.append(c_dir.replace('/', '\/'))
					self.count_ignore_dirs += 1

					print u"DROPBOX: Директория '%s' игнорируется." % c_dir
			else:
			
				if not self.checkDir(self.targetPath + c_dir):
					if not self.createDir(self.targetPath + c_dir):
						self.cryExit(u'DROPBOX: Невозможно создать директорию: %d' % self.targetPath + c_dir)
					else:
						self.count_create_dirs += 1
					
				if len(files) is not 0:
					for file in files:
					
						filename = (self.targetPath + c_dir + '/' + file).encode('utf-8')
						self.count_find_files += 1
						
						if len(self.ignoreFiles) is not 0 and file in self.ignoreFiles:
							self.count_ignore_files += 1
							print u"DROPBOX: Игнорируется файл '%s'" % filename
							
						elif len(self.ignoreExt) is not 0 and re.findall('|' . join(self.ignoreExt) + '$', file):
							self.count_ignore_files += 1
							print u"DROPBOX: Игнорируется файл '%s'" % filename
							
						else:
							_msg = u'DROPBOX: Передача файла "%s" ..............' % filename
							try:
								path_file = os.path.expanduser(os.path.join(dir, file));
								from_file = open(path_file, "rb")
								self.api_client.put_file(self.targetPath + c_dir + '/' + file, from_file, True)
								self.count_transfer_files += 1	
								_msg += u'Успешно!'
							except Exception: 
								_msg += u'ОШИБКА!'
								pass
								
							print _msg

		self.stats()
					
	def stats(self):
		print u"STATS:"
		print u" ----- Всего найдено папок: %d" % self.count_find_dirs
		print u" ----- Cоздано директорий в DROPBOX: %d" % self.count_create_dirs
		print u" ----- Проигнорировано директорий: %d" % self.count_ignore_dirs
		print u" ----- Всего найдено файлов: %d" % self.count_find_files
		print u" ----- Скопировано файлов в DROPBOX: %d" % self.count_transfer_files
		print u" ----- Проигнорировано файлов: %d" % self.count_ignore_files
		
	def checkDir(self, path):
		try:
			responeJSON = json.loads(json.dumps(self.api_client.metadata(path , None)))
		except Exception: 
			responeJSON = []
			pass

		if 'is_dir' not in responeJSON or not responeJSON['is_dir']:
			return False
			
		return True;
		
	def createDir(self, path):
		print u"DROPBOX: Директория '%s' не существует. Пробуем создать." % path
		try:
			self.api_client.file_create_folder(path)
			print u"DROPBOX: Директория '%s' успешно создана." % path
			
			return True;
			
		except Exception: 
			print u"DROPBOX: Невозможно создать директорию '%s'!" % path
			pass
			
		return False;
		
	def cryExit(msg = u'Работа скрипта заверешна. Устраните все ошибки!'):
		exit(msg);

def force_utf8_hack():

	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	for attr in dir(locale):
		if attr[0:3] != 'LC_':
			continue
			
		aref = getattr(locale, attr)
		locale.setlocale(aref, '')
		(lang, enc) = locale.getlocale(aref)
		
		if lang != None:
			try:
				locale.setlocale(aref, (lang, 'UTF-8'))
			except:
				os.environ[attr] = lang + '.UTF-8'

force_utf8_hack()
		
def main():
    if APP_KEY == '' or APP_SECRET == '' or ACCESS_TOKEN == '':
        exit(u'LOCAL: Укажите все необходимые параметры (APP_KEY, APP_SECRET, ACCESS_TOKEN)')
		
	if not os.path.isdir(args['sourcePath']):
		exit(u'LOCAL: Исходная директория ' + args['sourcePath'] + ' не найдена');
		
    DropBoxUpload(APP_KEY, APP_SECRET, ACCESS_TOKEN, args)
	
if __name__ == '__main__':
    main()
	
print "------------------------------------------------------------\n"

