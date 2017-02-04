from scipy.stats import norm
import math

class DataSet(object):

	def __init__ (self, data, alphabet):
		self.data = data
		self.alphabet = alphabet
		self.max = max(data)
		self.min = min(data)
		self.dataSize = len(data)
		self.alphabetSize = len(alphabet)

	# 1) Equal Width Discretization (EWD)	
	def EWD (self):
		scale = self.max - self.min + 1
		step = scale/self.alphabetSize;
		changes = [x*step + self.min for x in range(1,self.alphabetSize)]
		changes.append(self.max+1)
		return self.replace(self.data, changes)

	# 2) Equal Frequency Discretization (EFD)
	def EFD (self):
		step = self.dataSize / self.alphabetSize
		srt = sorted(self.data)
		changes = []
		
		for i in [ x*step for x in range(1,self.alphabetSize)]:
			changes.append( srt[round(i)] )
		changes.append(srt[-1]+1)	
		return self.replace(self.data, changes)

	# 4) Symbolic Aggregate Approximation (SAX)
	def SAX(self, newSize):
		PAA = self.PAA(newSize)
		u = sum(PAA) / newSize
		o = math.sqrt( sum([(x-u)**2 for x in PAA])/(newSize-1) )
		changes=[]
		for i in range(1,self.alphabetSize):
			changes.append( norm.ppf(i/self.alphabetSize, u, o) )
		changes.append(self.max+1)
		return self.replace(PAA, changes)
		
	def PAA (self, newSize):
		if newSize > self.dataSize:
			newSize=self.dataSize
		delta = self.dataSize / newSize
		PAA=[]
		for i in range( newSize ):
			m=0
			for j in range ( round(delta*i), round(delta*(i+1)) ):
				m += self.data[j]
			PAA.append(m / (round(delta*(i+1))-round(delta*i)) )
		return PAA

	def replace (self, data, changes):
		discrete = []
		for t in data:
			for i in range(self.alphabetSize):
				if t < changes[i]:
					discrete.append(self.alphabet[i])
					break
		return discrete
