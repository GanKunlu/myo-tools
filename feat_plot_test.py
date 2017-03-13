# -*- coding: gbk -*-
from tools.reader import *
from tools.featureExtract import FeatureExtractor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tools.MyPlot import DataPlotter
import os
slice = [600,1400]
ChanList = ['Raw-c0','Raw-c1','Raw-c2','Raw-c3','Raw-c4','Raw-c5','Raw-c6','Raw-c7']
featList = ['RMS','ZC','ARC0','ARC1','ARC2','ARC3'] 
path = os.getcwd()+'/data'
channels = 8

reader = FilesReader(channels, path)
extractor = FeatureExtractor(reader.fileNumber, slice[1]-slice[0], 10, featRavel = False)
emg = reader.loadFile('1.txt')
print(reader.filesLength)
sliceData = emg[slice[0]:slice[1],:]
rawFrame = pd.DataFrame(sliceData, columns = ChanList)

RMSfeat = extractor.RMSfeat(sliceData)
ZCfeat = extractor.ZCfeat(sliceData)
ARCfeat = extractor.ARCfeat(sliceData, False)
zipfeat = [RMSfeat,ZCfeat]
zipfeat.extend(ARCfeat)
columns = extractor.creatFeatName(featList, 8)
featplot = DataPlotter(np.hstack(zipfeat), columns, 431)


selectFeat = ['RMS-c0', 'RMS-c5', 'RMS-c7',\
				'ZC-c0', 'ZC-c5', 'ZC-c7',\
				'ARC1-c0','ARC1-c5','ARC1-c7']
selectChan = ['Raw-c0','Raw-c5','Raw-c7']


for i in range(len(selectChan)):
	featplot.newSubplot(431+i, rawFrame[selectChan[i]],xylabel=[u'采样点',selectChan[i]])
	#plt.title('ÌâÄ¿',fontproperties='SimHei')
	
for j in range(len(selectFeat)):
	featplot.subplot([4,3,4+j], [selectFeat[j]], xylabel=[u'采样点',selectFeat[j]])
	
plt.show()

