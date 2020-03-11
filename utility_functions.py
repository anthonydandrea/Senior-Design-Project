#!/usr/bin/python3


import csv, random


#Utility functions


#Determines the most probable output types of 
#the attributes in a given table, writes to file
def output_types(table, table_name, header):
	for i in header:
		x = determine_attribute_type(table[i])

	with open(table_name, 'w') as csvfile:
		fieldnames = ['db', 'table', '(types, probabilities)']
		


#Determines most probable output types in a table
def determine_attribute_type(column_in_table, num_samples):
	type_cnts = {}
	for i in range(num_samples):
		x = random.sample(column)
		if (x not in type_cnts):
			type_cnts[x] = 0
		type_cnts[x] += 1

	majority_t = max(type_cnts.values())
	for t in type_cnts:
		if t == majority_t:
			determined_type = t
	percentage = 100.0*majority_t/num_samples
	return (determined_type, percentage)