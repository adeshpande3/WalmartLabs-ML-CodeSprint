from __future__ import division
import scipy
import numpy as np
import pandas as pd 
import matplotlib.pyplot as ply 
import csv
import sys

#This program provides a machine learning based solution to Hackerrank's
#MLCodesprint compeition sponsored by WalmartLabs. In the competition, the 
#program's job is to make predictions for which shelves a product should
#be on, given characteristics about the product.

#Using pandas to read in the csv file. The original file given by Hackerrank
#was a TSV file but I manually changed it to a CSV file and excluded some
#of the categories. 
file = pd.read_csv("train.csv")

#At this point, file is a 12653 x 14 array. 
print(file.shape)

#Removing all the rows where there is a missing tag or missing
#product name
file = file[file.tag.notnull()] #Remove all examples with no tag
file = file[file['Product Name'].notnull()] #Remove examples with no product name
del file['item_id'] #Useless column

#This function replaces each value in the passed in category
#so that the missing values are 0 and the other values are 1
def replace(category):
	file[category].replace([None],[0],inplace=True)
	file[category][file[category] > 0] = 1

#Replace missing Artist ID's, Genre ID's, ISBN's, Literary
#Genre's, Recommended Location's, and Publisher's with 0 
#and replace every nonzero value with 1. 
replace('Artist ID')
replace('Genre ID')
replace('ISBN')
replace('Literary Genre')
replace('Recommended Location')
replace('Publisher')
replace('Recommended Use') #Almost all the products with a
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

######################################################################
# Processing Product Name
######################################################################

#This is the hardest one to process since (mostly) all of the product 
#names are unique. Therefore, we'll need a better way than just retreiving
#the top x number of product names. 

#TODO

######################################################################
# Processing Tags
######################################################################

#Contains all the tags.
YtrainTemp = np.asarray(file['tag'].tolist())
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
print Ytrain

del file['tag'] #Don't need the tags anymore
Xtrain = pd.np.array(file)
print Xtrain



#print(file['Product Name'].value_counts())
