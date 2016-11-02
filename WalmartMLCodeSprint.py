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

numTrainExamples = 