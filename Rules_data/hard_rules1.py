import csv
import usaddress
with open('rules_states.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    states_dict = {}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            states_dict[row[0].lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})] = row[1].lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        line_count +=1 
with open('rules_baby-names.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    names_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0 and int(row[0]) > 1940:
            names_set.add(row[1].lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "}))
        line_count +=1

f = open('rules_countries.txt','r')
country_set = set()
line_count = 0
f1 = f.readlines() 
for row in f1:    
    country_set.add(row.lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})[:-1])
    line_count +=1

with open('surnames.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    lnames_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            lnames_set.add(row[0].lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "}))
        line_count +=1

with open('uscities.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    city_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            city_set.add(row[0].lower().strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "}))
        line_count +=1

with open('suffixes.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    suffix_set = {'null':'null'}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            suffix_set[row[0].strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})] = row[1].strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        line_count +=1

with open('prefixes.csv', mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    prefix_set = {'null':'null'}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            prefix_set[row[0].strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})] = row[1].strip().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
        line_count +=1


def check_states(state):
    return state.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "}) in states_dict

def check_country(country):
    return country.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in country_set

def check_fname(names):
    return names.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in names_set
def check_lname(names):
    return names.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in lnames_set
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

def check_suffix(suff):
    return (suff.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in suffix_set)
def check_prefix(pre):
    return (pre.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in prefix_set)
def check_city(city):
    return (city.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})  in city_set)

def check_street(street):
    x = usaddress.parse(street)
    num = False
    streetname = False
    post = False
    for item in x:
        if item[1] == 'StreetNamePostType':
            post = True
        if item[1] == "StreetName":
            streetname = True
        if item[1] == "AddressNumber":
            num = True
    return num and streetname and post
    # x = street.split()
    # flag = False
    # for z in range(1, len(x)):
    #     if not x[z].isdigit() and isinstance(x[z], str):
    #         flag = True
    # return (x[0].isdigit()  and flag)    


print(check_street("1234 Fake address"), check_states("arIZON    a@@@"))
