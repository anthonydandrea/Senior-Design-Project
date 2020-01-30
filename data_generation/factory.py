import random as rd
import numpy as np
from faker import Faker


class Factory:
    def __init__(self):
        self.fake = Faker()

    def getPerson(self):
        init = self.fake.profile()
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
            "bloodType": init["blood_group"],
            "glasses": self.fake.boolean(64),
            "contacts": self.fake.boolean(11),
        }

    def getPeople(self, numPeople=10):
        people = []
        for i in range(numPeople):
            people.append(self.getPerson())

        return people

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
        end = "-" + str(age - 1) + "y"
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
    def _getHeight(self, sex=None, age=None):
        m_average = 69
        f_average = 64
        baby_constant = 24
        a_magic_constant = 9

        if age and age < 16:
            m_average = (m_average - baby_constant) * age / a_magic_constant
            f_average = (f_average - baby_constant) * age / a_magic_constant

        elif age == 0:  # for less than 12 months, either big baby or small infant
            m_average = baby_constant
            f_average = baby_constant

        if sex == "M":
            return round(np.random.normal(m_average, 2.5))
        elif sex == "F":
            return round(np.random.normal(f_average, 2))
        else:
            return round(np.random.normal((m_average + f_average) / 2, 2.25))

    # https://dqydj.com/weight-percentile-calculator-men-women/
    def _getWeight(self, sex=None, age=None):
        m_average = 189
        f_average = 161
        baby_constant = 9

        if age and age < 18:
            m_average *= age / 18
            f_average *= age / 18

        elif age == 0:  # for less than 12 months, either big baby or small infant
            m_average = baby_constant
            f_average = baby_constant

        if sex == "M":
            return round(np.random.normal(m_average, 25))
        elif sex == "F":
            return round(np.random.normal(f_average, 25))
        else:
            return round(np.random.normal((m_average + f_average) / 2, 25))
