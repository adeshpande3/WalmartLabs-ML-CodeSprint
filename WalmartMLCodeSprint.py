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
file = file[file.tag.notnull()]
file = file[file['Product Name'].notnull()]
del file['item_id']

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

#SELLER, ACTUAL COLOR, ITEM CLASS ID, MPAA RATING, 
#PRODUCT NAME, RECOMMENDED USE

Xtrain = pd.np.array(file)

#Contains all the tags.
Ytrain = np.asarray(file['tag'].tolist())

print(file['Recommended Use'])
