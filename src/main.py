from read import readDataset
from discretize import DataSet
from align import alignScore
from statistics import getStatistics
import pearson as pr
import cluster
import motifs
import os

import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

def getCountries(dataset):
	countries=[]
	for k in dataset:
		countries.append(k)
	return sorted(countries)

def discretizeSAX (dataset, alphabet, size):
	sax={}
	for k, v in dataset.items():
		data = DataSet (v,alphabet)
		#dataset[k] = data.PAA(300)
		sax[k] = data.SAX(size)
	return sax

def saveMatrix (matrix, filename):
	if not os.path.exists("../outputs/"):
		os.makedirs("../outputs/")
	out = open ("../outputs/"+filename+".dat", "w+")
	for line in matrix:
		for v in line:
			out.write(str(v))
			out.write(" ")
		out.write("\n")
	out.close()

def clusterHierarchical(d, countries, fname):
	corr = sp.spatial.distance.pdist(pd.DataFrame.transpose(d), 'correlation')
	cluster = sp.cluster.hierarchy.linkage(corr)
	plt.figure(figsize=(15, 17))
	plt.title('')
	plt.xlabel('')
	plt.ylabel('')
	sp.cluster.hierarchy.dendrogram(
		cluster,
		leaf_rotation=90.,
		leaf_font_size=20.,
		labels=countries,
		color_threshold = 0.001
	)
	if not os.path.exists("../outputs/"):
		os.makedirs("../outputs/")
	plt.savefig("../outputs/"+fname+".png")

 
print ("Reading file...")
dataset = readDataset ("../inputs/GlobalLandTemperaturesByMajorCity.csv")
cities = getCountries(dataset[0])


print ("Getting statistics...")
statistics = getStatistics(dataset[0])


print ("Ploting Datasets...")
#initial unchanged datasets
for city,temps in dataset[0].items():
    plt.figure(figsize=(30, 5))
    dates = dataset[1][city]
    plt.plot( dates, temps, linestyle='-', color='b', marker="o")#, t, t**2, 'bs', t, t**3, 'g^')
    #index=range(0,len(london),12)
    plt.savefig("../outputs/initial/"+city.replace(" ","_")+".png")


print ("Discretizations:")
#sax 4, 1500 datasets
for city,temps in dataset[0].items():
    dates = dataset[1][city]
    mx = max(temps)
    mn = min(temps)
    alf4 = range(4)
    alf20 = range(20)
    disc4 = DataSet(temps, alf4)
    disc20 = DataSet(temps, alf20)
    saxsize=len(temps)//12
    sax4 = disc4.SAX(saxsize)
    sax20 = disc20.SAX(saxsize)
    a4="ACGT"
    a20="ACDEFGHIKLMNPQRSTVWY"
    saxLabel4=""
    saxLabel20=""
    for c in sax4:
        saxLabel4+=a4[c]
    for c in sax20:
        saxLabel20+=a20[c]
    
    plt.figure(figsize=(30, 5))    
    plt.yticks(sax4,saxLabel4)
    plt.plot( [dates[x*12] for x in range(len(temps)//12)], sax4, linestyle='-', color='b', marker="o")
    plt.savefig("../outputs/sax/4_"+city.replace(" ","_")+".png")
    plt.close()
    
    plt.figure(figsize=(30, 5))
    plt.yticks(sax20,saxLabel20)
    plt.plot( [dates[x*12] for x in range(len(temps)//12)], sax20, linestyle='-', color='b', marker="o")
    plt.savefig("../outputs/sax/20_"+city.replace(" ","_")+".png")
    plt.close()
    

'''
london = dataset[0]["London"]
mx = max(london)
mn = min(london)
alf = [ mn + (mx-mn)*x/3 for x in range(4)] # A, C, G, T
disc = DataSet(dataset[0]["London"], alf)
ewd = disc.EWD()
efd = disc.EFD()
saxsize=len(london)//12
sax = disc.SAX(saxsize)

plt.figure(figsize=(15, 5))
plt.plot( dataset[1]["London"][-60:], london[-60:], linestyle='-', color='b', marker="o")#, t, t**2, 'bs', t, t**3, 'g^')
plt.plot( dataset[1]["London"][-60:], ewd[-60:], linestyle='--', color='g', marker="s")#, t, t**2, 'bs', t, t**3, 'g^')
plt.plot( dataset[1]["London"][-60:], efd[-60:], linestyle='-.', color='r', marker="*")#, t, t**2, 'bs', t, t**3, 'g^')
index=range(0,len(london),12)
plt.plot( [dataset[1]["London"][x] for x in index][-5:], sax[-5:], linestyle=':', color='y', marker="^")#, t, t**2, 'bs', t, t**3, 'g^')
plt.savefig("../outputs/LondonTest.png")
    
'''
mx = statistics["tempInfo"]["maximum"]
mn = statistics["tempInfo"]["minimum"]


alfabeto={ 4:"ACGT", 20:"ACDEFGHIKLMNPQRSTVWY"}

for alf_size in [4,20]:
    
    alf = [ mn + (mx-mn)*x/(alf_size-1) for x in range(alf_size)]
    alfString= alfabeto[alf_size]
    for paa_len in [50,100,250,500,1000,1500]:
        
        print("")
        tmpstr=str(alf_size)+"_"+str(paa_len)
        
        df = pd.DataFrame()
        
        for city, series in dataset[0].items():
            df[city] = DataSet(series, alf).SAX(paa_len)
            
           
        corr = pr.getDistanceMatrix(df)
        
        print("Ploting pearson correlation...")
        
        pr.plotHeatmap(corr, "distances/"+tmpstr+".png")
            
        print("Ploting hierarchical clustering...")
        try:
            clusterHierarchical(df, cities, "hierarchical/"+tmpstr)
        except:
            pass
        
        counts={x:[0]*paa_len for x in alfString}
        
        sax = discretizeSAX (dataset[0], alfString, paa_len)
        
        for city,serie in sax.items():
            for i in range( paa_len ):
                counts[ serie[i] ][i]+=1
        
        print("Ploting motif area chart...")
        motifs.plotAreaChart(counts,"../outputs/motifs/"+tmpstr+".png")
        
        if alf_size == 4 and paa_len == 100:
            tmp=sax
            print ( motifs.findMotifs(sax, 9, 0.1) )
        
        if alf_size == 20 and paa_len in [50, 1500]:
            print("Ploting k-medoids clustering...")
            for k in range(2,6):
                M, C = cluster.k_medoids(corr.as_matrix(),k)
            
                d={}
                for group, cities in C.items():
                    d[group] = []
                    for city in cities:
                        cityName = corr.columns[city] 
                        d[group].append( (dataset[2][cityName]) )
                        
                cluster.drawMap(d,"../outputs/mapa/"+str(paa_len)+"_"+str(k)+".png")
        
        print("Ploting sequence logos...")
        motifs.saveAsFasta(sax, "../outputs/seqLogos/fasta/"+tmpstr+".fasta")
        #Usar só em ambientes Unix:
        #motifs.generatePNG()     
        