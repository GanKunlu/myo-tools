# -*- coding: gbk -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataPlotter(object):
	''' 
	myplot class 
	subNum: The input number of subplot
	colormap: the color we select to plot
	__init__: creat a figure, when subNum is not defalut value, the size of figure will change automaticly
	plot(): plot multi-signals based pandas's Dataframe, selectcol is the select columns.
	subplot(): subplot will use plot function to plot one sub-figure
	newSubplot(): subplot with other new data 
	_xylabel(): add label to the figure. when use chinese label, input must be unicode String.
	'''
	def __init__(self, data, columns,subNum = -1):
		self.data = self._creatDatafram(data, columns)
		self.colormap = ['#4C72B0','#55A868','#C44E52','#8172B2','#CCB974','#64B5CD','#A38CF4','#F461DD']
		sns.set_style("whitegrid")
		if subNum == -1:
			plt.figure(figsize=(4.5,3))
		else:
			high = (subNum/100)*2.3
			width = (subNum%100)/10*3.5
			plt.figure(figsize=(width,high))
		
	def _creatDatafram(self, data, columns):
		return pd.DataFrame(data, columns = columns)
		
	def _xylabel(self, xylabel):
		if isinstance(xylabel[0], unicode):
			plt.xlabel(xylabel[0], fontproperties='SimHei')
		else:
			plt.xlabel(xylabel[0])
		if isinstance(xylabel[1], unicode):
			plt.ylabel(xylabel[1], fontproperties='SimHei')
		else:
			plt.ylabel(xylabel[1])
	
	def plot(self, selectcol, xylabel = [], ls=10*['-'], lw=10*[1]):
		for index, col in enumerate(selectcol):
			plt.plot(self.data[col], self.colormap[index], label='$'+col+'$',ls=ls[index],lw = lw[index])
		if xylabel != []:
			self._xylabel(xylabel)
		return plt
		
	def legend(self):
		plt.legend(ncol = 3, fontsize = 'medium')
		
	def subplot(self, number, selectcol, xylabel = [],ls=10*['-'],lw=10*[1]):
		if isinstance(number,int):
			plt.subplot(number)
		else:
			assert len(number) == 3,'subplot datatype error!'
			plt.subplot(number[0],number[1],number[2])
		self.plot(selectcol, xylabel = xylabel,ls = ls,lw = lw)
	
	def newSubplot(self,number,data,color = 0, label = '', xylabel = [],ls='-',lw=1):
		if isinstance(number,int):
			plt.subplot(number)
		else:
			assert len(number) == 3,'subplot datatype error!'
			plt.subplot(number[0],number[1],number[2])
		plt.plot(data, self.colormap[color], label=label,ls=ls,lw = lw)
		if xylabel != []:
			self._xylabel(xylabel)
		return plt
