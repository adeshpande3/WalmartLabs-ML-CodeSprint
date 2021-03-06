from __future__ import division
from sklearn.neighbors import KNeighborsClassifier
import scipy
import numpy as np
import collections
import pandas as pd 
import csv
import sys

#This program provides a machine learning based solution to Hackerrank's
#MLCodesprint compeition sponsored by WalmartLabs. In the competition, the 
#program's job is to make predictions for which shelves a product should
#be on, given characteristics about the product.

#Using pandas to read in the csv file. The original file given by Hackerrank
#was a TSV file but I opened it in Excel and saved it as a CSV

#This function replaces each value in the passed in category
#so that the missing values are 0 and the other values are 1
def replace(file, category):
	file[category].replace([None],[0],inplace=True)
	file[category][file[category] > 0] = 1
	return file

def preprocessDataset(filename, testOrTrain):
	file = pd.read_csv(filename)

	#Removing all the rows where there is a missing tag or missing
	#product name
	if (testOrTrain == "Train"):
		file = file[file.tag.notnull()] #Remove all examples with no tag
	file = file[file['Product Name'].notnull()] #Remove examples with no product name
	del file['item_id'] #Useless column
	del file['Color'] #Useless column
	del file['Recommended Room'] #Useless column
	del file['Synopsis'] #Useless column
	del file['actual_color'] #Useless column

	if (testOrTrain == "Test"):
		del file['Actors']
		del file['Aspect Ratio']
		del file['Product Long Description']
		del file['Product Short Description']
		del file['Short Description']
	#Replace missing Artist ID's, Genre ID's, ISBN's, Literary
	#Genre's, Recommended Location's, and Publisher's with 0 
	#and replace every nonzero value with 1. 
	file = replace(file,'Artist ID')
	file = replace(file,'Genre ID')
	file = replace(file,'ISBN')
	file = replace(file,'Literary Genre')
	file = replace(file,'Recommended Location')
	file = replace(file,'Publisher')
	file = replace(file,'Recommended Use') #Almost all the products with a
	#not null value are in the televsision category

	#Value_counts gets a list of the most frequently used values in
	#the given category

	######################################################################
	# Processing MPAA Ratings
	######################################################################

	ratingCounts = file['MPAA Rating'].value_counts().index.tolist()
	listRatings = []
	#Get the top 14 ratings
	for i in range(0,14): listRatings.append(ratingCounts[i])
	listValuesForRatings=[.5,1.5,1,2,.75,.5,1.5,2,1,.5,.75,1.5,1.5,2]
	file['MPAA Rating'].replace([None],[0],inplace=True)
	file['MPAA Rating'].replace(listRatings,listValuesForRatings,inplace=True)

	######################################################################
	# Processing Actual Color
	######################################################################

	colorCounts = file['Actual Color'].value_counts().index.tolist()
	listColors = []
	#Get the top 14 colors
	for i in range(0,14): listColors.append(colorCounts[i])
	listValuesForColors=[1,1.5,.1,.2,.3,1,.4,.5,.6,.7,1,.1,.8,.9]
	file.loc[~file['Actual Color'].isin(listColors), 'Actual Color'] = 0
	file['Actual Color'].replace(listColors,listValuesForColors,inplace=True)

	######################################################################
	# Processing Item Class ID
	######################################################################

	file.loc[~file['Item Class ID'].isin(['19','1']), 'Item Class ID'] = 0
	file['Item Class ID'].replace(['19','1'],[1,2],inplace=True)

	######################################################################
	# Processing Sellers
	######################################################################

	sellerCounts = file['Seller'].value_counts().index.tolist()
	listSellers=[]
	#Get the top 20 sellers
	for i in range(0,20): listSellers.append(sellerCounts[i])
	listValuesForSellers=([x * 0.2 for x in range(0, 20)])
	file.loc[~file['Seller'].isin(listSellers), 'Seller'] = 0
	file['Seller'].replace(listSellers,listValuesForSellers,inplace=True)
	return file

def findMostCommon(file):
	######################################################################
	# Processing Product Name
	######################################################################

	#This is the hardest one to process since (mostly) all of the product 
	#names are unique. Therefore, we'll need a better way than just retreiving
	#the top x number of product names. The main goal is to be able to parse
	#the product name and figure out a category or label to assign it to.

	#The approach will be to go through every product name, and store,
	#in a list, every word that appears. This is ONLY done for the training
	#set. 
	m_Common=[]
	allProductNames = file['Product Name'].tolist()
	allWords=[]
	for product in allProductNames:
		words = product.split()
		for word in words:
			allWords.append(word)
	counter=collections.Counter(allWords)
	m_Common = counter.most_common(500)
	for index in range(0,len(m_Common)):
		if (index >= len(m_Common)): break
		if (len(m_Common[index][0]) <= 2):
			m_Common.pop(index)
	return m_Common

def processProductName(common, file):
	allProductNames = file['Product Name'].tolist()
	for index in range(0,len(allProductNames)):
		print index
		for index2 in range(0,len(common)):
			if (allProductNames[index].find(common[index2][0]) != -1):
				file['Product Name'].replace([allProductNames[index]],[index2 * .1],inplace=True)
				break
			if (index2 == len(common) - 1):
				file['Product Name'].replace([allProductNames[index]],[0],inplace=True)
				break
	return file

trainFile = preprocessDataset("train.csv","Train")
testFile = preprocessDataset("test.csv","Test")
mostCommon = findMostCommon(trainFile)
trainFile = processProductName(mostCommon,trainFile)
testFile = processProductName(mostCommon,testFile)

######################################################################
# Processing Tags
######################################################################

#Contains all the tags.
YtrainTemp = np.asarray(trainFile['tag'].tolist())
Ytrain=[]
for y in YtrainTemp:
	tempString = y
	indexOfComma = tempString.find(',')
	if (indexOfComma == -1):
		#Theres only one value in the tag
		indexOfRightBracket = tempString.index(']')
		Ytrain.append(int(tempString[1:indexOfRightBracket]))
	else:
		#Theres more than one value and we have to just 
		#take the first one
		Ytrain.append(int(tempString[1:indexOfComma]))

#Converting unique tags to values between 1 and 31
counter=collections.Counter(Ytrain)
listLabels=counter.keys()
listValuesForLabels=([x for x in range(1, len(counter.values()) + 1)])
df1 = pd.DataFrame({'labels': Ytrain})
df1['labels'].replace(listLabels,listValuesForLabels,inplace=True)
Ytrain = df1['labels'].tolist()	

del trainFile['tag'] #Don't need the tags anymore
Xtrain = pd.np.array(trainFile)
Xtest = pd.np.array(testFile)
numTestExamples = len(Xtest)

######################################################################
# Applying Machine Learning
######################################################################

Xtrain = np.asarray(Xtrain)
Xtest = np.asarray(Xtest)
Ytrain = np.asarray(Ytrain)

print Xtrain.shape
print Xtest.shape
print Ytrain.shape

neigh = KNeighborsClassifier(n_neighbors=103)
neigh.fit(Xtrain, Ytrain)
results = np.ones((numTestExamples,2))
counter = 10593 #item_id the test set starts from
justPredictions=[]

for x in range(0,numTestExamples):
	justPredictions.append((neigh.predict(Xtest[x]))[0])
	results[x,1] = (neigh.predict(Xtest[x]))[0]
	results[x,0] = counter
	counter = counter + 1

df2 = pd.DataFrame({'labels': justPredictions})
df2['labels'].replace(listValuesForLabels,listLabels,inplace=True)
labelsList = df2['labels'].tolist()
for x in range(0,numTestExamples):
	results[x,1] = labelsList[x]

#Saving predictions into a test file that can be uploaded to Hackerrank
with open("tags.tsv", "w") as record_file:
    record_file.write("item_id\ttag\n")
    for temp in results:
        record_file.write(str(temp[0])+"\t"+"["+str(temp[1])+"]"+"\n")