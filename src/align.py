# Needleman–Wunsch algorithm

def match (a,b,size):
	return size - abs(a-b)
	
def gap ():
	return -8

def alignScore (seqa, seqb, alphabet):
	lena, lenb = len(seqa), len(seqb)
	size = len (alphabet)
	matrix = [ [0]*(lena+1) for x in range(lenb+1) ]
	for j in range(lena):
		matrix[0][j+1] = matrix[0][j] + gap()
	
	for i in range(lenb):
		matrix[i+1][0] = matrix[i][0] + gap()
	
	for i in range (1,lenb+1):
		for j in range (1,lena+1):
			diag = matrix[i-1][j-1] + match(j,i,size)
			top = matrix[i-1][j] + gap()
			left = matrix[i][j-1] + gap()
			matrix[i][j] = max ( [diag, top, left] )
	return matrix [i][j]
