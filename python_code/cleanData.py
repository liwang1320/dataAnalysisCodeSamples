
#characteristics noticed in the data that can simplify it

# Properties to check
# aIF is always 1
# aDD is always 0
# fN is NA
# iC is 0

# conclusion:
# feautureName is always NA
# iC is always 0
# ~0.1% of aIF and aDD are different

#we will create a new dataframe without those two columns
#called dataSmartAlertFeaturesLess


import pandas as pd 
import math

fileName = "alert.csv"

data = pd.read_csv(fileName)
totalPoints = 0
nonOneIndex1 = []
nonOneIndex2 = []
index1 = 0
index2 = 0

# checking aIF is 1 case
aIFCol = data['aIF']

isAlwaysOne = True
count = 0
for i in aIFCol:
	totalPoints+=1
	if not(i):
		isAlwaysOne = False
		count+=1
		nonOneIndex1.append(index1)
	index1 +=1 

if isAlwaysOne:
	print("aIF is always 1")
else:
	print("aIF is not always 1")
	print("there are " + str(count) + " non-one instances")
print("\n")



#checking aDD is 0 case
aDDCol = data['aDD']
isAlwaysZero = True
count = 0
for i in aDDCol:
	if i:
		# print(i)
		isAlwaysZero = False
		count+=1
		nonOneIndex2.append(index2)
	index2 +=1

if isAlwaysZero:
	print("aDD is always 0")
else:
	print("aDD is not always 0")
	print("there are " + str(count) + " non-zero instances")
print("\n")

print("out of " + str(totalPoints) + " points")

print("\n")
print("first one indexes")
print(nonOneIndex1[:25])
print("\n")
print("second one indexes")
print(nonOneIndex2[:25])

#checking fN is always NA
fNCol = data['fN']
isAlwaysNA = True
count = 0
for i in fNCol:
	if not math.isnan(i):
		isAlwaysNA = False
		count+=1


if isAlwaysNA:
	print("fN is always NA")
else:
	print("fN is not always NA")
	print("there are " + str(count) + " non-zero instances")
print("\n")



#checking iC is 0 case
iCCol = data['iC']
isAlwaysZero = True
count = 0
for i in iCCol:
	if i:
		isAlwaysZero = False
		count+=1


if isAlwaysZero:
	print("iC is always 0")
else:
	print("iC is not always 0")
	print("there are " + str(count) + " non-zero instances")
print("\n")

fileName = "alertsFeaturesLess.csv"

data.pop("fN")
data.pop("iC")
data.pop("Unnamed: 0")

data.to_csv(fileName)









