#!/usr/bin/python

import csv
#Base case: query when there is an exact match
#No errors, no unique identifiers

DATA_FILES = ["data_1000_samples.csv"]

def user_input():
	search_attribute = input("Input attribute value or property name: ")
	return search_attribute

def search_file(file, term):
	#dialect = csv.Sniffer().sniff(file.read(1024))
	file.seek(0)
	reader = csv.DictReader(file)#, dialect=dialect)
	for row in reader:
		if term in row.values():
			print(row)

def query(field_value):
	for f in DATA_FILES:
		with open(f) as csv_f:
			search_file(csv_f, field_value)

if __name__=="__main__":
	s = user_input()
	query(s)