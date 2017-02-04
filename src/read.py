from datetime import datetime

def readDataset (filepath):	
	'''
	count=0
	expectedMax = 600000
	'''
	dataset = {}
	dates = {}
	coordinates = {}
	with open(filepath, encoding="utf8") as infile:
		infile.readline()
		for line in infile:
			# split csv columns:
			row = line.strip().split(",")
			
			# check valid temperature
			temp = row[1]
			if len(temp) > 0:

				# get city
				city = row[3]

				if city in ["London", "Madrid", "Moscow", "Paris", "New Delhi", "Peking", "Tokyo",
					"Los Angeles", "New York", "Toronto", "Lima", "Rio De Janeiro", "Cairo", "Luanda", "Sydney" ]:
					tmp=4
					if city[0]=="\"":	
						while city[1:].find("\"")==-1:
							city+=","+row[tmp]
							tmp+=1
						city=city[1:-1]
					lat = row[tmp+1]
					lng = row[tmp+2]
                    	
					if city not in coordinates:
						coordinates[city] = (lat,lng)
					# add temperature to dictionary
					if city in dataset:
						dataset[city].append(float(temp))
						dates[city].append(datetime.strptime(row[0], "%Y-%m-%d"))
					else:
						dataset[city]=[float(temp)]
						dates[city]=[datetime.strptime(row[0], "%Y-%m-%d")]
		
			# print read percentage
			'''
			count+=1
			if count%(expectedMax/100)==0:
				print( int(count/expectedMax*100),"%")
			'''
	infile.close()
	return (dataset, dates,coordinates)
