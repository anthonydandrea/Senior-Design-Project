#!/usr/bin/python3
#from sklearn import cluster
from kmodes.kmodes import KModes
import numpy as np
import csv, json, codecs

#https://github.com/nicodv/kmodes

# Description: 
# Input: standardized/cleaned data/metadata
# Output: clustering of groups as dictionary
#     of mappings, i.e. attribute to set
#     of other attributes 
# Functions: utility/ML 


def file_processor(file, outp, given_data=None):
	final = []
	if (outp):
		with open(file, 'w',encoding='utf-8') as strout:
			for x in given_data:
				final.append(x)
			strout.write(str(final))
		
	else:
		with open(file, 'r') as csvfile:
			csvfile.seek(0)
			reader = csv.reader(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			data = []
			for row in reader:
				data.append(row)
		return data

def run_naive_clustering(data, n_clus):
	
	km = KModes(n_clusters = n_clus, init='Huang', n_init=5, verbose=1)
	grouping = km.fit_predict(data)
	return grouping


if __name__=="__main__":	
	data = file_processor("data_1000_samples.csv", False)
	groupings = run_naive_clustering(data, 4)
	file_processor("clusterings.txt", True, groupings)