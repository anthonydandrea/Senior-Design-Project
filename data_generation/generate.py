from keyboard import Keyboard
from factory import Factory
import json
import os
import random as rd
import time
import csv

tic = time.process_time()

# 2000 ~ 5 seconds
# 12000 ~ 26 seconds
# 30000 ~ 70 seconds
numPeople = 1000

outputCsvPath = os.path.join(os.path.dirname(__file__), "../data_1000_samples.csv")

K = Keyboard()
F = Factory()

fieldnames = list(F.getPerson().keys())

# these keys will be considered "important", and reliably typo-free
safeKeys = ["ssn", "sex", "bloodType"]
typoProbability = 0.025

numPeopleWithTypos = 0
totNumTypos = 0
totYield = 0

with open(outputCsvPath, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for p in F.getPeople(numPeople):
        totYield += 1
        typoGiven = False
        for k, v in p.items():
            if k not in safeKeys and type(v) == type(""):
                if rd.random() < typoProbability:
                    typoGiven = True
                    idxs = set()
                    numTypos = rd.randint(1, min(2, len(v)))
                    totNumTypos += numTypos

                    while len(idxs) < numTypos:
                        idxs.add(rd.randint(0, len(v) - 1))

                    # print(p[k],'-->',end=' ')
                    newVal = list(p[k])
                    for i in idxs:
                        newVal[i] = K.getTypo(newVal[i])

                    p[k] = "".join(newVal)
                    # print(p[k])

        if typoGiven:
            numPeopleWithTypos += 1

        writer.writerow(p)


toc = time.process_time()

print()
print("Total number of persons: {}".format(totYield))
print("Total number of persons with typos: {}".format(numPeopleWithTypos))
print("Total number of typos: {}".format(totNumTypos))

print("\nTotal runtime: {} seconds".format(str(toc - tic)))
print("\n\nok")

