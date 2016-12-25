from tools.reader import *
from tools.featureExtract import FeatureExtractor
import os
import matplotlib.pyplot as plt
# load FilesReader and FeatureExtractor class
path = os.getcwd()+"\data"
print(path)
reader = FilesReader(8,path)
extractor = FeatureExtractor(reader.fileNumber, 60, 10)
# init Mat:
feats = np.array([])
labels = np.array([])

for classIndex, fileName in enumerate(reader.files):
	# load file:
	dataMat = reader.loadFile(fileName)
	# gesture segmentation:
	segMat = extractor.segmentation(dataMat, classIndex)
	# init:
	featMat = np.array([])
	for segIndex, seg in enumerate(segMat):
		# extract RMS, ZC, ARC features:
		RMSfeat = extractor.RMSfeat(seg)
		ZCfeat = extractor.ZCfeat(seg)
		ARCfeat = extractor.ARCfeat(seg)
		featVector = np.hstack((RMSfeat,ZCfeat,ARCfeat))
		# feats splice:
		featMat = extractor.dynamicSplice(featMat, featVector, segIndex)
	# generate labels:
	tempLabels = extractor.creatLabels(classIndex, len(featMat))
	# feat array and label array splice:
	feats = extractor.dynamicSplice(feats, featMat, classIndex)
	labels = extractor.dynamicSplice(labels, tempLabels, classIndex, axis = 1)

print(feats[0])
print(labels[0])