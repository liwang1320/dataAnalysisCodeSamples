
#characteristics noticed in the data that can simplify it

# Properties to check
# activeInactiveFlag is always 1
# alertDefaultIsDisabled is always 0
# featureName is NA
# isCurrent is 0

# conclusion:
# feautureName is always NA
# isCurrent is always 0
# ~0.1% of activeInactiveFlag and alertDefaultIsDisabled are different

#we will create a new dataframe without those two columns
#called dataSmartAlertFeaturesLess


import pandas as pd 
import math

fileName = "../Avera_data/dataSmartAlert.csv"

data = pd.read_csv(fileName)
totalPoints = 0
nonOneIndex1 = []
nonOneIndex2 = []
index1 = 0
index2 = 0

# checking activeInactiveFlag is 1 case
activeInactiveFlagCol = data['activeInactiveFlag']

isAlwaysOne = True
count = 0
for i in activeInactiveFlagCol:
	totalPoints+=1
	if not(i):
		isAlwaysOne = False
		count+=1
		nonOneIndex1.append(index1)
	index1 +=1 

if isAlwaysOne:
	print("activeInactiveFlag is always 1")
else:
	print("activeInactiveFlag is not always 1")
	print("there are " + str(count) + " non-one instances")
print("\n")



#checking alertDefaultIsDisabled is 0 case
alertDefaultIsDisabledCol = data['alertDefaultIsDisabled']
isAlwaysZero = True
count = 0
for i in alertDefaultIsDisabledCol:
	if i:
		# print(i)
		isAlwaysZero = False
		count+=1
		nonOneIndex2.append(index2)
	index2 +=1

if isAlwaysZero:
	print("alertDefaultIsDisabled is always 0")
else:
	print("alertDefaultIsDisabled is not always 0")
	print("there are " + str(count) + " non-zero instances")
print("\n")

print("out of " + str(totalPoints) + " points")

print("\n")
print("first one indexes")
print(nonOneIndex1[:25])
print("\n")
print("second one indexes")
print(nonOneIndex2[:25])

#checking featureName is always NA
featureNameCol = data['featureName']
isAlwaysNA = True
count = 0
for i in featureNameCol:
	if not math.isnan(i):
		isAlwaysNA = False
		count+=1


if isAlwaysNA:
	print("featureName is always NA")
else:
	print("featureName is not always NA")
	print("there are " + str(count) + " non-zero instances")
print("\n")



#checking isCurrent is 0 case
isCurrentCol = data['isCurrent']
isAlwaysZero = True
count = 0
for i in isCurrentCol:
	if i:
		isAlwaysZero = False
		count+=1


if isAlwaysZero:
	print("isCurrent is always 0")
else:
	print("isCurrent is not always 0")
	print("there are " + str(count) + " non-zero instances")
print("\n")

fileName = "../Avera_data/dataSmartAlertFeaturesLess.csv"

data.pop("featureName")
data.pop("isCurrent")
data.pop("Unnamed: 0")

data.to_csv(fileName)









