# WalmartLabs-ML-CodeSprint

https://www.hackerrank.com/contests/walmart-codesprint-ml/challenges/products-shelves-tagging

Hackerrank contest where participants have to develop a machine learning solution to the problem of putting products of a certain type on certain shelves, given characteristics about the product.  

Hackerrank provides two files (train.tsv and test.tsv) for the contestants. Looking at the files, I noticed that there was a lot of missing data and a lot of formatting errors with the train file. I decided to cut down the number of features that I would consider for each product. The features that I used are:

Seller, Actual Color, Artist ID, Genre ID, ISBN, Item Class ID, Literary Genre, MPAA Rating, Product Name, Publisher, Recommended Location, and Recommended Use. (14 Features In Total)

The label for each product is the tags column, which tells you what shelf each of the training examples(products) went on. 
