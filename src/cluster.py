import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def latToPercent(lat):
    g = float( lat[:-1].strip() )
    p = g / (90*2)
    if "N" in lat:
        return 0.5 - p
    elif "S" in lat:
        return 0.5 + p
    return -1

def lngToPercent(lng):
    g = float( lng[:-1].strip() )
    p = g / (180*2)
    if "E" in lng:
        return 0.5 + p
    elif "W" in lng:
        return 0.5 - p
    return -1

def drawMap(kmedoid, filename):
    #dicinário cor:[ (lat,lng), ... ]
    color=["#0000ff","#00ff00","#ffff00","#ff0000","#00ffff"]
    img = plt.imread("../map.jpg", format="jpeg")
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')
    plt.axis('off')
    ax.imshow(img, interpolation='nearest')
    for k,v in kmedoid.items():
        for city in v:
            city = ( lngToPercent(city[1])*img.shape[1], latToPercent(city[0])*img.shape[0] )
            circ = Circle(city,25,color=color[k])
            ax.add_patch(circ)
            
    plt.savefig(filename, dpi=250)
            

def k_medoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape

    if k > n:
        raise Exception('too many medoids')
    # randomly initialize an array of k medoid indices
    M = np.arange(n)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

    # return results
    return M, C
    
    
#drawMap({1:[("52.24N","0.00W")],2:[("49.03N","2.45E")],3:[("40.99N","4.26W")],4:[("55.45N","36.85E")]},
        #"../outputs/mapa/output.png")

def hierarquical(distances, filename):
	cluster = sp.cluster.hierarchy.linkage(distances)
	plt.figure(figsize=(15, 17))
	sp.cluster.hierarchy.dendrogram(
		cluster,
		leaf_rotation=90.,
         color_threshold = 0.001
	)
	plt.savefig(filename)