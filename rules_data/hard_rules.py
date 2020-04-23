import csv
import usaddress
import re
import phonenumbers
import os
import sys
from dateutil.parser import parse
from pathlib import Path
from fuzzywuzzy import fuzz

rules_data_path = str(Path('../rules_data').resolve())

with open(rules_data_path+"/rules_states.csv", mode="r") as csv_file:
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
with open(rules_data_path+"/rules_baby-names.csv", mode="r") as csv_file:
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

f = open(rules_data_path+"/rules_countries.txt", "r")
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

with open(rules_data_path+"/surnames.csv", mode="r") as csv_file:
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

with open(rules_data_path+"/uscities.csv", mode="r") as csv_file:
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

with open(rules_data_path+"/suffixes.csv", mode="r") as csv_file:
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

with open(rules_data_path+"/prefixes.csv", mode="r") as csv_file:
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
        if not zip[0:5].isdigit():
            return False

        if len(zip) == 5:
            return True
        elif len(zip) == 10:
            return zip[6:].isdigit()
    return False


def check_country(country):
    return _normalize(country) in country_set


def check_date(s):
    try:
        parse(s, fuzzy=False)
        return True
    except:
        return False


def check_sex(sex):
    return _normalize(sex) in ["m", "f"]


def check_phonenumber(number):
    try:
        num = phonenumbers.parse(number, "US")
        return phonenumbers.is_possible_number(num)
    except:
        return False


def check_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def check_bloodtype(bloodtype):
    return _normalize(bloodtype) in ["a-", "a+", "b-", "b+", "ab-", "ab+", "o-", "o+"]


def check_eyecolor(color):
    return _normalize(color) in ["blue", "green", "dark brown", "brown", "hazel"]


def check_ethnicity(ethnicity):
    for val in [
        "white",
        "hispanic",
        "latino",
        "black",
        "african american",
        "asian",
        "native american",
        "alaskan native",
        "native hawaiian",
        "pacific islander",
        "two or more races",
        "other"
    ]:
        # print(fuzz.partial_ratio(ethnicity, val))
        if fuzz.partial_ratio(ethnicity, val) > 75:
            print(ethnicity)
            return True

    return False


def check_age(s):
    try:
        num = int(s)
        return num >= 0 and num <= 125
    except:
        return False


def check_height(s):
    # for format 5' 11"
    # if bool(re.match(r"[1-8]' *[0-2]*\" *", s)):
    #     return True
    try:
        num = int(s)
        # babies >= 12 inches, grown adults <= 272 cm
        return num >= 12 and num <= 272
    except:
        return False


def check_weight(s):
    try:
        num = int(s)
        return num < 800
    except:
        return False


def check_glasses(s):
    if _normalize(s) in ["yes", "no", "true", "false", "none"]:
        return True

    return False


fn = {
    "age": check_age,
    "bloodType": check_bloodtype,
    "city": check_city,
    "country": check_country,
    "date": check_date,
    "email": check_email,
    "ethnicity": check_ethnicity,
    "eyecolor": check_eyecolor,
    "fname": check_fname,
    "glasses": check_glasses,
    "height": check_height,
    "lname": check_lname,
    "phone": check_phonenumber,
    "prefix": check_prefix,
    "sex": check_sex,
    "ssn": check_ssn,
    "state": check_states,
    "street": check_street,
    "suffix": check_suffix,
    "weight": check_weight,
    "zip": check_zip
}


def get_possible_keys(info):
    keys = []
    for key, func in fn.items():
        if func(info):
            keys.append(key)
    return keys


if __name__ == "__main__":
    tests = ["542678"]
    for t in tests:
        print(check_phonenumber(t))
