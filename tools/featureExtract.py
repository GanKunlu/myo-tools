# -*- coding: utf-8 -*-
import numpy as np
class FeatureExtractor(object):
	'''A class contains some feature extraction mehod
	'''
	def __init__(self, gestNumber, gestSize, winSize, featRavel = True):
		assert gestSize % winSize == 0, "winSize输入错误!"
		self.gestSize = gestSize
		self.winSize = winSize
		self.startList = [0]*gestNumber
		self.endList = [-1]*gestNumber
		if featRavel == True:
			self.featRavel = True
		else:
			self.featRavel = False
		
	def __repr__(self):
		return 'FeatureExtract(gestSize={0.gestSize!r},winSize={0.winSize!r})'.format(self)
	
	def setStratEnd(self, startList, endList):
		self.startList = startList
		self.endList = endList
	
	def segmentation(self, data, index, ravel = False):
		gStart = self.startList[index]
		gEnd = self.endList[index]
		pruneMat = data[gStart:gEnd,:]
		normValue = len(pruneMat) % self.gestSize
		segNumber = (len(pruneMat) - normValue) // self.gestSize
		if normValue != 0:
			tempMat = pruneMat[:-normValue:1,:]
		else:
			tempMat = pruneMat
		if ravel == True:
			tempMat = tempMat.ravel()
			segMat = np.hsplit(tempMat, segNumber)
		else:
			segMat = np.vsplit(tempMat, segNumber)
		return segMat
	
	def _RMS(self, data):
		assert len(data) > 1,"输入数组维数必须大于1!"
		return np.sqrt(np.mean(np.square(data),axis = 0))
		
	def _ZC(self, data):
		assert len(data) > 1,"输入数组维数必须大于1!"
		pieceMove1 = np.vstack((data[1::,:], np.zeros((1,len(data[0])))+1))
		ZCFeat = np.sum((-np.sign(data) * np.sign(pieceMove1)+1)/2,axis = 0)
		return ZCFeat
		
	def _ARC3ord(self, orinArray):
		tValue = len(orinArray)
		AR_coeffs = np.polyfit(range(tValue),orinArray,3)
		return AR_coeffs
		
	def _ARC3(self, data):
		return np.apply_along_axis(self._ARC3ord, 0, data)	
	
	def _seg2win(self, segData):
		splitSize = self.gestSize/self.winSize
		return np.vsplit(segData, splitSize)
		
	def _featMat2ravel(self, featData):
		if self.featRavel == True:
			featData = featData.ravel(order='F')
		return featData
		
	def RMSfeat(self, segData):
		featData = np.array([])
		for index, winData in enumerate(self._seg2win(segData)):
			featData = self.dynamicSplice(featData, self._RMS(winData), index)
		return self._featMat2ravel(featData)
		
	def ZCfeat(self, segData):
		featData = np.array([])
		for index, winData in enumerate(self._seg2win(segData)):
			featData = self.dynamicSplice(featData, self._ZC(winData), index)
		return self._featMat2ravel(featData)
	
	def ARCfeat(self, segData, strack = True):
		featData = np.array([])
		ARC = [0]*4
		for index, winData in enumerate(self._seg2win(segData)):
			for ARindex, ARcor in enumerate(self._ARC3(winData)):
				ARC[ARindex] = self.dynamicSplice(ARC[ARindex], ARcor, index)
		if strack == True:
			featData = np.vstack(ARC)
			return self._featMat2ravel(featData)
		else:
			assert self.featRavel == False, "arc各系数分开存储时，不允许对各通道特征进行矩阵拉直"
			return ARC
	
	def creatLabels(self, classIndex, length):
		return np.zeros(length) + classIndex
		
	def dynamicSplice(self, mat, dynamicMat, index, axis = 0):
		if axis == 0:
			if index == 0:
				mat = dynamicMat
			else:
				mat = np.vstack((mat, dynamicMat))
		elif axis == 1:
			if index == 0:
				mat = dynamicMat
			else:
				mat = np.hstack((mat, dynamicMat))
		return mat
	
	def creatFeatName(self, nameList,channels):
		columns = []
		for name in nameList:
			columns.extend([name+'-c'+str(i) for i in range(channels)])
		return columns
			
	
			