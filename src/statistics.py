def mean (values):
	return sum(values)/len(values)

def median (values):
	return sorted(values)[len(values)//2]

def mode (values):
	return max( [(x, values.count(x)) for x in set(values)], key=lambda item:item[1] )[0]

def srange (values):
	return max(values)-min(values)

def tempInfo (dataset):
	tmps = []
	for key in dataset:
		tmps += dataset[key]
	return {
		"minimum": min(tmps),
		"maximum": max(tmps),
		"average": sum(tmps)/len(tmps)
	}

def seriesInfo (dataset):
	counts = []
	for key in dataset:
		counts.append( len(dataset[key]) )
	return {
		"nTimeSeries":len(counts),
		"counts":counts,
		"mean": mean(counts), 
		"median": median(counts),
		"mode": mode(counts),
		"range": srange(counts)
	}

def getStatistics (dataset):
	return {
		"tempInfo":tempInfo(dataset),
		"seriesInfo": seriesInfo(dataset)
	}



