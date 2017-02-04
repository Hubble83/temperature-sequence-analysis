import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
'''
def getScores(dataset, alf):
	cities=[]
	for k in dataset:
		cities.append(k)
	nCities = len (cities)

	globalAlign = []
	for i in range(nCities):
		globalLine = []
		for j in range (i):
			v = pearsonr( dataset[cities[i]], dataset[cities[j]] )
			# NOTE: alignScore is very slow
			#v = alignScore ( dataset[cities[i]], dataset[cities[j]], alf )
			globalLine.append( v )
		globalAlign.append(globalLine)
	return globalAlign
'''
def getDistanceMatrix(dataset):
	corr = dataset.corr(method='pearson')
	corr = corr.applymap(lambda x: 1-x)
	return corr

def plotHeatmap(corr,filename):
	mask = np.zeros_like(corr, dtype=np.bool)
	mask[np.triu_indices_from(mask)] = True

	f, ax = plt.subplots(figsize=(9, 8))
    
	sns.heatmap(corr, mask=mask, cmap="winter_r", vmax=2,
				square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
	if not os.path.exists("../outputs/"):
		os.makedirs("../outputs/")
	f.savefig("../outputs/"+filename)
	plt.close(f)