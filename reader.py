# -*- coding: utf-8 -*-
# @author: Gan, 2016/10/26
import numpy as np
import re
import os 
import sys
reload( sys )
sys.setdefaultencoding('utf-8')

class FilesReader(object):
	'''
	Read data from txt files,every file named with Serial number of the gesture.
	this class can read all the files in a path.
	'''

	def __init__(self, columns, path = "defult" ):
		self.columns = columns
		if path == "defult":
			self.path = os.getcwd()
		else:
			self.path = path
		self.fileList = []
		self.fileNumber = 0	
		self.filesLength = {}
		self._nameSortMethod = lambda x:int(x[:-4])
		self._CreatFileList()
	def __repr__(self):
		return 'FilesReader(columns={0.columns!r},path={0.path!s})'.format(self)
		
	def _CreatFileList(self):
		OriFileList = os.listdir(self.path)
		self.fileList =[file for file in OriFileList if file.endswith(".txt")] 
		self.fileList.sort(key = self._nameSortMethod)
		self.fileNumber = len(self.fileList)
		for file in self.fileList:
			self.filesLength[file] = 0
			
	@property
	def files(self):
		return self.fileList
		
	@property	
	def allFilesData(self):
		matList = []
		for fileIndex, fileName in enumerate(self.fileList):
			matList.append(self.loadFile(fileName))
		return 	matList
		
	def loadFile(self,fileName):
		file = open(self.path +'/'+fileName,'r')
		# match the data in file.read()
		matchList = re.findall(r'[0-9.-]+',file.read())
		tempMat = np.array(matchList,dtype = 'float')
		# calculate the length of the file
		fileLength = len(tempMat)/self.columns
		# reshape the data
		dataMat = np.reshape(tempMat,(fileLength,self.columns))
		self.filesLength[fileName] = fileLength
		return dataMat

		