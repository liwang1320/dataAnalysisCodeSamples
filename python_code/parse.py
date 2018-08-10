
#this doc will parse the avera dataSmartAlert.txt file
#creates a csv with the column names

import pandas as pd

file = 'Alert'

dataFile = open('../data' + file + '.txt')

#Make csv from the data
firstLine = True
data = {}
fieldsInOrder = []

#for testing
stop = 1000
# it = 0
lineLength = 0
its = 1

for line in dataFile:
	if firstLine:
		fields = line.split("|")
		lineLength = len(fields)
		print(fields)
		for field in fields:
			data[field] = []
			fieldsInOrder.append(field)
		firstLine = False

	else:
		dataPoint = line.split("|")
		if len(dataPoint)!= lineLength:
			print("found a bad line")
			print(str(its))
			print(len(dataPoint))
			print("\n")
			continue
		for i in range(len(dataPoint)):
			var = fieldsInOrder[i]
			vec = data[var]
			vec.append(dataPoint[i])
			data[var] = vec
	its+=1
	# it+=1
	if its>stop:
		break


## dict to dataframe, dataframe to csv

csv_name = '../data' + file + '_test.csv'

dataFrameData = pd.DataFrame.from_dict(data)
dataFrameData.to_csv(csv_name)
