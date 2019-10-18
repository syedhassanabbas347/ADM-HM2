# importing libraries
import json
import pandas as pd
import matplotlib.pyplot as plt

result = {}; secResult = {}; teamsID = {}; dictApp = {}


# import and parsing files
teams = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\teams.json")
teamsJS = json.loads(teams.read())
matches = pd.read_json("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\matches_England.json")

# creating a first step result dictionary
for i in range(len(teamsJS)):
    if (teamsJS[i]["area"]["name"] == "England" or teamsJS[i]["area"]["name"] == "Wales") and teamsJS[i]["type"] != "national":
        result[teamsJS[i]["name"]] = [0]
        teamsID[teamsJS[i]["name"]] = teamsJS[i]["wyId"]
        secResult[teamsJS[i]["name"]] = [0, 0]
        dictApp[teamsJS[i]["name"]] = [0, 0]

# calculating points
dictMatches = matches.sort_values(by=["gameweek"])
for i in range(len(dictMatches["teamsData"])):
    l = list(dictMatches["teamsData"][i].keys())
    winner = dictMatches["winner"][i]
    if winner == 0:
        for sq in teamsID.keys():
            if teamsID[sq] == int(l[0]):
                result[sq].append(result[sq][len(result[sq]) - 1] + 1)
        for sq in teamsID.keys():
            if teamsID[sq] == int(l[1]):
                result[sq].append(result[sq][len(result[sq]) - 1] + 1)
    else:
        for sq in teamsID.keys():
            if teamsID[sq] == int(l[0]):
                if int(l[0]) == winner:
                    result[sq].append(result[sq][len(result[sq]) - 1] + 3)
                else:
                    result[sq].append(result[sq][len(result[sq]) - 1] + 0)
        for sq in teamsID.keys():
            if teamsID[sq] == int(l[1]):
                if int(l[1]) == winner:
                    result[sq].append(result[sq][len(result[sq]) - 1] + 3)
                else:
                    result[sq].append(result[sq][len(result[sq]) - 1] + 0)

# calculating series of victories and losses for each team
for sq, points in result.items():
    for i in range(len(points)-1):
        if points[i+1] == (points[i] + 3):
            dictApp[sq][0] += 1
            if dictApp[sq][1] != 0:
                if dictApp[sq][1] > secResult[sq][1]:
                    secResult[sq][1] = dictApp[sq][1]
                dictApp[sq][1] = 0
        if points[i+1] == points[i]:
            dictApp[sq][1] += 1
            if dictApp[sq][0] != 0:
                if dictApp[sq][0] > secResult[sq][0]:
                    secResult[sq][0] = dictApp[sq][0]
                dictApp[sq][0] = 0
        if points[i+1] == (points[i] + 1):
            if dictApp[sq][1] > secResult[sq][1]:
                secResult[sq][1] = dictApp[sq][1]
            dictApp[sq][1] = 0
            if dictApp[sq][0] > secResult[sq][0]:
                secResult[sq][0] = dictApp[sq][0]
            dictApp[sq][0] = 0

# finding the teams with the higtest series of wins and losses
sWin = ""; sLoss = ""; mWins = 0; mLosses = 0
for sq, series in secResult.items():
    if series[0] > mWins:
        mWins = series[0]
        sWin = sq
    if series[1] > mLosses:
        mLosses = series[1]
        sLoss = sq

# showing the result
plt.xlabel("Num. Giornata")
plt.ylabel("Punti")
for key, values in result.items():
    if key == sWin or key == sLoss:
        plt.plot(values, label=key, linewidth=3.5)
    else:
        plt.plot(values, label=key)
plt.legend()
plt.show()