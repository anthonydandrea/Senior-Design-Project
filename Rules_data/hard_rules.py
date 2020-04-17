import csv
import usaddress
import re
import phonenumbers

from dateutil.parser import parse

def __init__(self):
    pass

with open("rules_states.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    states_dict = {}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            states_dict[
                row[0]
                .lower()
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            ] = (
                row[1]
                .lower()
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1
with open("rules_baby-names.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    names_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0 and int(row[0]) > 1940:
            names_set.add(
                row[1]
                .lower()
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1

f = open("rules_countries.txt", "r")
country_set = set()
line_count = 0
f1 = f.readlines()
for row in f1:
    country_set.add(
        row.lower()
        .strip()
        .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})[:-1]
    )
    line_count += 1

with open("surnames.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    lnames_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            lnames_set.add(
                row[0]
                .lower()
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1

with open("uscities.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    city_set = set()
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            city_set.add(
                row[0]
                .lower()
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1

with open("suffixes.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    suffix_set = {"null": "null"}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            suffix_set[
                row[0]
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            ] = (
                row[1]
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1

with open("prefixes.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    prefix_set = {"null": "null"}
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            prefix_set[
                row[0]
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            ] = (
                row[1]
                .strip()
                .translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
            )
        line_count += 1


###########################################


def _normalize(s):
    return s.lower().translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})


def check_ssn(ssn):
    if len(ssn) == 11 or len(ssn) == 9:
        if len(ssn) == 11:
            return ssn[0:3].isdigit() and ssn[4:6].isdigit() and ssn[7:].isdigit
        else:
            return ssn.isdigit()
    return False


def check_fname(name):
    return _normalize(name) in names_set


def check_lname(name):
    return _normalize(name) in lnames_set


def check_prefix(pre):
    return _normalize(pre) in prefix_set


def check_suffix(suff):
    return _normalize(suff) in suffix_set


def check_street(street):
    x = usaddress.parse(street)
    num = False
    streetname = False
    post = False
    for item in x:
        if item[1] == "StreetNamePostType":
            post = True
        if item[1] == "StreetName":
            streetname = True
        if item[1] == "AddressNumber":
            num = True
    return num and streetname and post


def check_city(city):
    return _normalize(city) in city_set


def check_states(state):
    return _normalize(state) in states_dict


def check_zip(zip):
    if len(zip) == 10 or len(zip) == 5:
        if len(zip) == 10:
            return zip[0:5].isdigit() and zip[6:].isdigit()
        else:
            return zip.isdigit()
    return False


def check_country(country):
    return _normalize(country) in country_set


def check_date(s):
    try:
        parse(s, fuzzy=True)
        return True
    except ValueError:
        return False


def check_sex(sex):
    return _normalize(sex) in ["m", "f"]


def check_phonenumber(number):
    try:
        phonenumbers.parse(number, "US")
        return True
    except:
        return False


def check_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def check_bloodtype(bloodtype):
    return _normalize(bloodtype) in ["a-", "a+", "b-", "b+", "ab-", "ab+", "o-", "o+"]


def check_eyecolor(color):
    return _normalize(color) in ["blue", "green", "dark brown", "brown", "hazel"]


def check_ethnicity(ethnicity):
    return _normalize(ethnicity) in [
        "white",
        "hispanic/latino",
        "black/african american",
        "asian",
        "native american/alaskan native",
        "native hawaiian/pacific islander",
        "two or more races",
        "other",
    ]
fn = [check_bloodtype,
    check_city,
    check_country, 
    check_date,
    check_email,
    check_ethnicity,
    check_eyecolor,
    check_fname,
    check_lname,
    check_phonenumber,
    check_prefix,
    check_sex,
    check_ssn,
    check_states,
    check_street,
    check_suffix,
    check_zip]
st = ["blood type",
    "city",
    "country",
    "date ",
    "email",
    "ethnicity",
    "eye color",
    "fname",
    "lname",
    "phone number",
    "prefix",
    "sex",
    "ssn",
    "states",
    "street",
    "suffix",
    "zip",]
def get_possible_keys(info):
    keys = []
    for x in range(len(fn)):
        if fn[x](info):
            keys.append(st[x])
    return keys


