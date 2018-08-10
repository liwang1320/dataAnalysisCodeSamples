import random
import pandas as pd
import numpy as np



dataName = 'MAP'

data =  dataName + '_only.csv'

df = pd.read_csv(data, low_memory=False) #this is so we don't guess the type of the info of the column, also because it changes
colnames = list(df)

#take in a time stamp and returns the number of minutes as an int
def parseTime(timeStamp):
	timeString = str(timeStamp)
	timeList = timeString.split(":")
	hourSecs = int(timeList[0])*3600
	minuteSecs = int(timeList[1])*60
	secSecs = int(timeList[2])
	return hourSecs+minuteSecs+secSecs

#assuming that we are at the end of a day, we add a day
def diffTime(startTime, endTime):
	if endTime<startTime:
		endTime = endTime + (60*60*24)
	return endTime - startTime


#for getAlarmGeneral
# get the number of alerts, averageDuration, averageTimeBetweenAlerts
def calculateAlarmInfoGeneral(keyDict):
	print(keyDict)
	tTime = keyDict['tTime']
	tOffset = keyDict['tOffset']
	reactTime = keyDict['rTime']
	reactOff = keyDict['rOffset']

	numAlerts = len(tTime)

	if numAlerts==1:
		print("we have a key with only 1 alert")
		print("tTime: " + tTime[0])
		return 1, 0, 0, 0, 0, 0

	print(tTime)
	last = parseTime(tTime[0])
	timeBetweenAlerts = []
	for i in range(1, numAlerts):
		this = parseTime(tTime[i])
		# we dont need to check that rs are in order, cuz it doesn't matter, and t offsets were ordered
		if tOffset[i-1] > tOffset[i]:
			print("the t offset decreased, something is weird")
		timeBetweenAlerts.append(diffTime(last, this))
		last = this
	print("this is the time between in seconds")
	print(timeBetweenAlerts)
	print("\n")

	minTimeBetween = min(timeBetweenAlerts)
	maxTimeBetween = max(timeBetweenAlerts)

	timeBetweenArr = np.array(timeBetweenAlerts)
	q1 = np.percentile(timeBetweenArr, 25)
	q2 = np.percentile(timeBetweenArr, 50)
	q3 = np.percentile(timeBetweenArr, 75)
	#because its the difference between 2 times

	return numAlerts, minTimeBetween, maxTimeBetween, q1, q2, q3


## We assume that the data separated by uKey and in chronological order
# Returns a dictionary with boxplot info
def getAlarmGeneral(df):
	endLastKey = False #the first one is a newKey
	keySet = df['uKey']

	print(keySet)
	lastKey = 0
	first = True
	dataSetLength = len(keySet)
	tTimeSet = df['tDateTime24Hr']
	tOffsetSet = df['tDateOffset']
	rTimeSet = df['reactiveDateTime24Hr']
	rOffsetSet = df['reactiveDateOffset']
	returnDict = {'uKey':[], 'numberAlerts':[], 'minTimeBetween': [], 'maxTimeBetween': [], '1stQ': [], 'median':[], '3rdQ':[]}
	keydict = {'tTime':[], 'tOffset':[], 'rTime':[], 'rOffset':[]}
	for i in range(len(keySet)):


		thisKey = keySet[i]
		if lastKey!=thisKey and not first: #this will be false for the first value
			endLastKey = True
		first = False
		if endLastKey:
			#do the end last key
			# print(keydict)
			numAlerts, minTimeBw, maxTimeBw, Q1, Q2, Q3 = calculateAlarmInfoGeneral(keydict)
			
			#update uKey
			keyUpdate = returnDict['uKey']
			keyUpdate.append(lastKey)
			returnDict['uKey'] = keyUpdate

			#update numberAlerts
			numberAlertsUpdate = returnDict['numberAlerts']
			numberAlertsUpdate.append(numAlerts)
			returnDict['numberAlerts'] = numberAlertsUpdate

			minTimeUpdate = returnDict['minTimeBetween']
			minTimeUpdate.append(minTimeBw)
			returnDict['minTimeBetween'] = minTimeUpdate

			#update numberAlerts
			maxTimeUpdate = returnDict['maxTimeBetween']
			maxTimeUpdate.append(maxTimeBw)
			returnDict['maxTimeBetween'] = maxTimeUpdate


			q1Update = returnDict['1stQ']
			q1Update.append(Q1)
			returnDict['1stQ'] = q1Update

			#update numberAlerts
			medianUpdate = returnDict['median']
			medianUpdate.append(Q2)
			returnDict['median'] = medianUpdate

			q3Update = returnDict['3rdQ']
			q3Update.append(Q3)
			returnDict['3rdQ'] = q3Update


			#clear the keyDict
			keydict = {'tTime':[], 'tOffset':[], 'rTime':[], 'rOffset':[]}
			endLastKey = False

		#handle this key; get the information from the different sets
		#handle this key; get the information from the different sets
		trigTimeUpdate = keydict['tTime']
		trigOffsetUpdate = keydict['tOffset']
		reactTimeUpdate = keydict['rTime']
		reactOffsetUpdate = keydict['rOffset']

		#make the new lists
		trigTimeUpdate.append(tTimeSet[i])
		trigOffsetUpdate.append(tOffsetSet[i])
		reactTimeUpdate.append(rTimeSet[i])
		reactOffsetUpdate.append(rOffsetSet[i])

		#update the dictionary
		keydict['tTime'] = trigTimeUpdate
		keydict['tOffset'] = trigOffsetUpdate
		keydict['rTime'] = reactTimeUpdate
		keydict['reationOffset'] = reactOffsetUpdate

		#update everything
		lastKey = thisKey

	#add the last one
	numAlerts, minTimeBw, maxTimeBw, Q1, Q2, Q3 = calculateAlarmInfoGeneral(keydict)
	
	#update uKey
	keyUpdate = returnDict['uKey']
	keyUpdate.append(lastKey)
	returnDict['uKey'] = keyUpdate

	#update numberAlerts
	numberAlertsUpdate = returnDict['numberAlerts']
	numberAlertsUpdate.append(numAlerts)
	returnDict['numberAlerts'] = numberAlertsUpdate

	#update min time 
	minTimeUpdate = returnDict['minTimeBetween']
	minTimeUpdate.append(minTimeBw)
	returnDict['minTimeBetween'] = minTimeUpdate

	#update max time
	maxTimeUpdate = returnDict['maxTimeBetween']
	maxTimeUpdate.append(maxTimeBw)
	returnDict['maxTimeBetween'] = maxTimeUpdate

	#update q1
	q1Update = returnDict['1stQ']
	q1Update.append(Q1)
	returnDict['1stQ'] = q1Update

	#update numberAlerts
	medianUpdate = returnDict['median']
	medianUpdate.append(Q2)
	returnDict['median'] = medianUpdate

	q3Update = returnDict['3rdQ']
	q3Update.append(Q3)
	returnDict['3rdQ'] = q3Update


	return returnDict


# getAlarmGeneral(df)
# takes in a dictionary and writes the csv that can make boxplots
# flip rows and columns 
# returns the dictionary of column number to user id
def convertToExcel(rawDict):
	minSet = rawDict['minTimeBetween']
	q1Set = rawDict['1stQ']
	medianSet = rawDict['median']
	q3Set = rawDict['3rdQ']
	maxSet = rawDict['maxTimeBetween']
	userSet = rawDict['uKey']

	boxplotDict = {}
	usersToColumn = {}
	numVals = len(userSet)
	for i in range(numVals):
		#make a new column for each ukey
		newCol = [minSet[i], q1Set[i]-minSet[i], medianSet[i]-q1Set[i], q3Set[i]-medianSet[i], maxSet[i]-q3Set[i]]

		#add column to the dictionary
		boxplotDict[i] = newCol
		usersToColumn[userSet[i]] = i 

	csv_name = dataName + '_boxplots.csv'

	analyzedDataFrame = pd.DataFrame.from_dict(boxplotDict)
	analyzedDataFrame.to_csv(csv_name)

	return usersToColumn

print(convertToExcel(getAlarmGeneral(df)))



















