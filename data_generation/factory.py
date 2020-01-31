import random as rd
import numpy as np
from faker import Faker
import os
import json


class Factory:
    def __init__(self):
        self.fake = Faker()
        self.usedSSNs = set()
        self.targets = []

        peopleFilePath = os.path.join(os.path.dirname(__file__), "people.json")

        with open(peopleFilePath) as json_file:
            data = json.load(json_file)
            for person in data:
                self.targets.append(person)
                if person["ssn"] in self.usedSSNs:
                    raise Exception(
                        "Duplicate SSN used in people.json, this is not allowed."
                    )
                self.usedSSNs.add(person["ssn"])

    def getPerson(self):
        init = self.fake.profile()
        while init["ssn"] in self.usedSSNs:
            init["ssn"] = self.fake.ssn()
        self.usedSSNs.add(init["ssn"])

        age = self._getAge()
        dob = self._getBirthdateFromAge(age)
        dob_str = str(dob.month) + "/" + str(dob.day) + "/" + str(dob.year)

        return {
            "ssn": init["ssn"],
            "firstName": self.fake.first_name(),
            "lastName": self.fake.last_name(),
            "prefix": self.fake.prefix() if self.fake.boolean(90) else None,
            "suffix": self.fake.suffix() if self.fake.boolean(5) else None,
            "streetAddress": self.fake.street_address(),
            "city": self.fake.city(),
            "state": self.fake.state(),
            "zip": self.fake.postalcode(),
            "country": "United States",
            "DOB": dob_str,
            "sex": init["sex"],
            "phone": self.fake.phone_number(),
            "email": init["mail"],
            "age": age,
            "height (inches)": self._getHeight(init["sex"], age),
            "weight (pounds)": self._getWeight(init["sex"], age),
            "ethnicity": self._getEthnicity(),
            "eyeColor": self._getEyeColor(),
            "bloodType": self._getBloodType(),
            "glasses": self.fake.boolean(64),
            "contacts": self.fake.boolean(11),
        }

    def getPeople(self, totPeople=10):
        numFakePeople = totPeople - len(self.targets)

        # the 1.2 is to statistically encourage the unlikely-yet-possible chance of several targets being appended to the end in a bunch.
        # becomes less significant as number of "fake" people increases
        targetFraction = 1.2 * len(self.targets) / totPeople
        targetIdx = 0

        for i in range(totPeople):
            if (rd.random() <= targetFraction and targetIdx < len(self.targets)) or (
                i >= numFakePeople and targetIdx < len(self.targets)
            ):
                targetIdx += 1
                yield self.targets[targetIdx - 1]
            else:
                yield self.getPerson()

        # just in case
        # for i in range(len(self.targets)):
        #     if targetIdx == len(self.targets):
        #         yield self.getPerson()
        #     else:
        #         targetIdx += 1
        #         yield self.targets[targetIdx - 1]

    def _getProbabilisticValueFromArray(self, arr):
        r = rd.random()
        tot = 0

        for val, prob in arr:
            tot += prob
            if tot >= r:
                return val

        # Just in case of 0.9999...
        return arr[rd.randint(0, len(arr) - 1)]

    # https://en.wikipedia.org/wiki/Race_and_ethnicity_in_the_United_States
    def _getEthnicity(self):
        groups = [
            ("White", 0.724),
            ("Hispanic/Latino", 0.163),
            ("Black/African American", 0.126),
            ("Asian", 0.048),
            ("Native American/Alaskan Native", 0.009),
            ("Native Hawaiian/Pacific Islander", 0.002),
            ("Two or more races", 0.029),
            ("Other", 0.062),
        ]

        return self._getProbabilisticValueFromArray(groups)

    # https://en.wikipedia.org/wiki/Blood_type_distribution_by_country
    def _getBloodType(self):
        types = [
            ("O+", 0.374),
            ("A+", 0.357),
            ("B+", 0.085),
            ("AB+", 0.034),
            ("O-", 0.066),
            ("A-", 0.063),
            ("B-", 0.015),
            ("AB-", 0.006),
        ]

        return self._getProbabilisticValueFromArray(types)

    # https://visual.ly/community/infographic/other/eye-color-demographics-usa
    def _getEyeColor(self):
        colors = [
            ("Blue", 0.32),
            ("Green", 0.12),
            ("Dark Brown", 0.25),
            ("Brown", 0.16),
            ("Hazel", 0.15),
        ]
        return self._getProbabilisticValueFromArray(colors)

    def _getBirthdateFromAge(self, age):
        start = "-" + str(age) + "y"
        end = "-" + str(age - 1) + "y" if age > 0 else "+1y"
        return self.fake.date_between(start, end)

    # https://www.statista.com/statistics/270000/age-distribution-in-the-united-states/
    def _getAge(self):
        ages = [
            (rd.randint(0, 14), 0.19),
            (rd.randint(15, 64), 0.67),
            (rd.randint(65, 100), 0.14),
        ]
        return self._getProbabilisticValueFromArray(ages)

    # https://dqydj.com/height-percentile-calculator-for-men-and-women/
    # https://icosep.org/wp-content/uploads/2016/03/boys-CHART-height-andweight-text.jpg
    def _getHeight(self, sex=None, age=None):
        m_average = 69
        f_average = 64
        baby_constant = 20
        child_height = 2.3 * (age - 2) + (34 if sex == "M" else 28)

        if age and age <= 17 and age >= 2:
            return round(child_height + round(np.random.normal(0, 2)))

        elif age and age < 2:  # for less than 24 months, either baby or infant
            return round(baby_constant + age * round(np.random.normal(6, 1)))

        if sex == "M":
            return round(np.random.normal(m_average, 2.5))
        elif sex == "F":
            return round(np.random.normal(f_average, 2))
        else:
            return round(np.random.normal((m_average + f_average) / 2, 2.25))

    # https://dqydj.com/weight-percentile-calculator-men-women/
    # https://icosep.org/wp-content/uploads/2016/03/boys-CHART-height-andweight-text.jpg
    def _getWeight(self, sex=None, age=None):
        m_average = 189
        f_average = 161
        baby_constant = 9
        child_weight = None

        if sex == "M":
            child_weight = 8.9 * (age - 2) + 28
        elif sex == "F":
            child_weight = 7.4 * (age - 2) + 26
        else:
            child_weight = 8.1 * (age - 2) + 27

        if age and age >= 2 and age <= 20:
            return round(child_weight)

        elif age and age < 2:  # for less than 12 months, either baby or infant
            return round(baby_constant + age * round(np.random.normal(18, 3)))

        if sex == "M":
            return round(np.random.normal(m_average, 25))
        elif sex == "F":
            return round(np.random.normal(f_average, 25))
        else:
            return round(np.random.normal((m_average + f_average) / 2, 25))
