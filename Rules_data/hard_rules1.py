import csv

with open('rules_states.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    states_dict = {}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            states_dict[row[0].lower()] = row[1].lower()
        line_count +=1 
with open('rules_baby-names.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    names_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0 and int(row[0]) > 1940:
            names_set.add(row[1].lower())
        line_count +=1

f = open('rules_countries.txt','r')
country_set = set()
line_count = 0
f1 = f.readlines() 
for row in f1:    
    country_set.add(row.lower()[:-1])
    line_count +=1

with open('surnames.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    lnames_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            lnames_set.add(row[0].lower())
        line_count +=1


def check_states(state):
    return state in states_dict

def check_country(country):
    return country  in country_set

def check_fname(names):
    return names in names_set
def check_lname(names):
    return names in lnames_set
def check_ssn(ssn):
    if len(ssn) == 11 or  len(ssn) == 9:
        if len(ssn) == 11:
            return  (ssn[0:3].isdigit() and ssn[4:6].isdigit() and ssn[7:].isdigit)
        else:
            return (ssn.isdigit())
    return False

def check_zip(zip):
    if len(zip) == 10 or  len(zip) == 5:
        if len(zip) == 10:
            return  (zip[0:5].isdigit() and zip[6:].isdigit())
        else:
            return (zip.isdigit())
    return False

    


    
