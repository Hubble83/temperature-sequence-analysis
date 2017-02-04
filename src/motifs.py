import os
import pandas as pd

def saveAsFasta (dataset, filename):
    f = open(filename,"w")
    for k,v in dataset.items():
        f.write(">"+k+"\n")
        f.write("".join(v)+"\n")
        
        
def generatePNG ():
    os.system("./seqLogos.sh")
    
def plotAreaChart(counts, filename):
    df = pd.DataFrame.from_dict(counts, orient='columns', dtype=None)
    ax = df.plot(kind='area', figsize=(30,5), stacked=True, colormap="autumn_r",
                 ylim=(0,15), use_index=False, yticks=[], xticks=[])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=20, prop={'size':14})
    fig = ax.get_figure()
    fig.savefig(filename)

def clone(dictionary):
    data={}
    for k,v in dictionary.items():
        data[k]=v
    return data
    
def findMotifs(data, W, P):
    if P>1 or P<0 or W<1: return []
    seqs=clone(data)
    num_seqs = len(seqs)
    res=[]
    while len(seqs) >= num_seqs*P:
        city, seq_0 = seqs.popitem()
        for i in range ( len(seq_0) - W + 1 ):
            count = 0
            motif = "".join(seq_0 [i:i+W])
            for k,seq in seqs.items():
                #if motif == seq[i:i+W]:
                if motif in "".join(seq):
                    count += 1
                if count/(num_seqs-1) >= P:
                    if motif not in res:
                        res.append(motif)
                    break
    return res
    
'''
di = { "A":"AAAACCCC",
       "B":"AAAACCCC",
       "C":"AACGAACG" }

print ( findMotifs(di,4,0.67) ) # []
print ( findMotifs(di,4,0.33) ) # ["AAAA", ..., "CCCC"]
print ( findMotifs(di,2,1) ) # ["AA","AC"]
print ( findMotifs(di,1,1) ) # ["A","C"] 
'''