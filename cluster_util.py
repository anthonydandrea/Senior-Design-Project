#!/usr/bin/python3
import json_utilities
import db_utilities

# Description: 
# Input: standardized/cleaned data/metadata
# Output: clustering of groups as dictionary
#     of mappings, i.e. attribute to set
#     of other attributes 
# Functions: utility/ML 


#def run_gibbs_sampling(param):
#	return


#split data available into numerical or categorical data
def split_by_type(samples):
	(flt, strg) = (0,0)
	for x in samples:
		try:
			float(x)
			flt += 1
		except: 
			strg += 1
	if (flt >> strg):
		#write the sample as a float



#run numerical clustering
def numerical_clustering():
#sample from each, catalog

#stat package?


#run categorical clustering - Bloom filter
#allows us to still use probabilistic ML
def categorical_clustering():
#https://pypi.org/project/bloom-filter/




if __name__=="__main__":

	