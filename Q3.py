# importing libraries
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def calcolaEta(birthDate):
    today = datetime.date.today()
    birth = datetime.date(int(birthDate[0:4]), int(birthDate[5:7]), int(birthDate[8:]))
    return int((today - birth).total_seconds()//31536000)

resultPar = {}; resultDef = {}; teamsId = {}
barplotList = [[], []]

# this is the part of the assignment where we have to create the barplot in which we show the distribution of the
# ages of the coaches

# import and parsing files
teams = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\teams.json")
teamsJS = json.loads(teams.read())
matches = pd.read_json("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\matches_England.json")
coaches = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\coaches.json")
coachesJS = json.loads(coaches.read())

# creating a first step result dictionary
for i in range(len(teamsJS)):
    if (teamsJS[i]["area"]["name"] == "England" or teamsJS[i]["area"]["name"] == "Wales") and teamsJS[i]["type"] != "national":
        resultPar[teamsJS[i]["name"]] = []
        resultDef[teamsJS[i]["name"]] = []
        teamsId[str(teamsJS[i]["wyId"])] = teamsJS[i]["name"]

# constructing a first part of the result
for i in range(len(matches)):
    cSqCasa = dict(list(matches["teamsData"][i].values())[0])["coachId"]
    cSqTras = dict(list(matches["teamsData"][i].values())[1])["coachId"]
    lApp = list(matches["teamsData"][i].keys())
    sqCasa = teamsId[lApp[0]]
    sqTras = teamsId[lApp[1]]
    if cSqCasa not in resultPar[sqCasa] and cSqCasa != 0:
        resultPar[sqCasa].append(cSqCasa)
    if cSqTras not in resultPar[sqTras] and cSqTras != 0:
        resultPar[sqTras].append(cSqTras)

# creation of the list of ages
for sq, coachIds in resultPar.items():
    for coach in coachIds:
        for i in range(len(coachesJS)):
            if coachesJS[i]["wyId"] == coach:
                resultDef[sq].append(calcolaEta(coachesJS[i]["birthDate"]))

# constructing data for the barplot
for ages in resultDef.values():
    for el in ages:
        if el not in barplotList[0]:
            barplotList[0].append(el)
            barplotList[1].append(1)
        else:
            barplotList[1][barplotList[0].index(el)] += 1

# showing the results
plt.xlabel("Age")
plt.ylabel("Number")
plt.bar(barplotList[0], barplotList[1], width=0.25)
plt.show()

# this is the part where I show the ten teams with the youngest coaches
result = {}

#
for sq, coach_ages in resultDef.items():
    if len(result) < 10:
        result[sq] = min(coach_ages)
    else:
        if min(coach_ages) <  max(result.values()):
            result[sq] = min(coach_ages)
            for key, value in result.items():
                if value == max(result.values()):
                    keyElRem = key
            result.pop(keyElRem)

# printing result
for key in result.keys():
    print(key)