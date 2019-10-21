# importing libraries
import json
import pandas as pd
import matplotlib.pyplot as plt

firResult = [["0-9", "9-18", "18-27", "27-36", "36-45", "45+", "45-54", "54-63", "63-72", "72-81", "81-90", "90+"],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
secResult = {}
thResult = {}


# import and parsing files
teams = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\teams.json")
teamsJS = json.loads(teams.read())
en_events = pd.read_json("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\events_England.json")
players = pd.read_json("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\players.json")

l1 = list(en_events[en_events["subEventId"] == 100]["id"])
l2 = list(en_events[en_events["subEventId"] == 35]["id"])
l3 = list(en_events[en_events["subEventId"] == 33]["id"])
lAppPar = []; lAppDef = []
lGoals = []
teamsID = {}
elRe = ""

# creating dictionaries that associate teams ids to their names
for i in range(len(teamsJS)):
    if (teamsJS[i]["area"]["name"] == "England" or teamsJS[i]["area"]["name"] == "Wales") and teamsJS[i]["type"] != "national":
        teamsID[teamsJS[i]["name"]] = teamsJS[i]["wyId"]
        secResult[teamsJS[i]["name"]] = 0

# creating a list that contain the ids of all shots
for el in l1:
    lAppPar.append(el)
for el in l2:
    lAppPar.append(el)
for el in l3:
    lAppPar.append(el)

# creating a list that contain the ids of all goals
for evId in lAppPar:
    tagEv = list(en_events[en_events["id"] == evId]["tags"])
    for i in range(len(tagEv[0])):
        if tagEv[0][i]["id"] == 101 or tagEv[0][i]["id"] == 102:
            lAppDef.append(evId)

# extracting values of interest
l = []
for evId in lAppDef:
    app = []
    app.append(int(en_events[en_events["id"] == evId]["eventSec"]))
    app.append(str(list(en_events[en_events["id"] == evId]["matchPeriod"])[0]))
    app.append(str(int(en_events[en_events["id"] == evId]["playerId"])))
    app.append(str(int(en_events[en_events["id"] == evId]["teamId"])))
    l.append(app)

for i in range(len(l)):
    if l[i][2] not in thResult.keys():
        thResult[l[i][2]] = []

# calculating results
for el in l:
    if el[1] != "1H": # all el[1] can be "1H" or "2H" (I test it)
        m = float(el[0]/60)
        if m < 9:
            firResult[1][6] += 1
            if 1 not in thResult[el[2]]:
                thResult[el[2]].append(1)
        if 9 <= m < 18:
            firResult[1][7] += 1
            if 2 not in thResult[el[2]]:
                thResult[el[2]].append(2)
        if 18 <= m < 27:
            firResult[1][8] += 1
            if 3 not in thResult[el[2]]:
                thResult[el[2]].append(3)
        if 27 <= m < 36:
            firResult[1][9] += 1
            if 4 not in thResult[el[2]]:
                thResult[el[2]].append(4)
        if 36 <= m < 45:
            firResult[1][10] += 1
            for sqName, sqId in teamsID.items():
                if sqId == int(el[3]):
                    secResult[sqName] += 1
            if 5 not in thResult[el[2]]:
                thResult[el[2]].append(5)
        if m >= 45:
            firResult[1][11] += 1
            if 6 not in thResult[el[2]]:
                thResult[el[2]].append(6)
    else:
        m = float(el[0]/60) + 45
        if m < 54:
            firResult[1][0] += 1
            if 7 not in thResult[el[2]]:
                thResult[el[2]].append(7)
        if 54 <= m < 63:
            firResult[1][1] += 1
            if 8 not in thResult[el[2]]:
                thResult[el[2]].append(8)
        if 63 <= m < 72:
            firResult[1][2] += 1
            if 9 not in thResult[el[2]]:
                thResult[el[2]].append(9)
        if 72 <= m < 81:
            firResult[1][3] += 1
            if 10 not in thResult[el[2]]:
                thResult[el[2]].append(10)
        if 81 <= m < 90:
            firResult[1][4] += 1
            if 11 not in thResult[el[2]]:
                thResult[el[2]].append(11)
        if m >= 90:
            firResult[1][5] += 1
            if 12 not in thResult[el[2]]:
                thResult[el[2]].append(12)

for i in range(10):
    m = min(secResult.values())
    for sq, goals in secResult.items():
        if goals == m:
            elRe = sq
    secResult.pop(elRe)

# showing the results of the first part
plt.xlabel("")
plt.ylabel("Number")
plt.bar(firResult[0], firResult[1], width=0.25)
plt.show()

# showing the results of the second part
print("\nTop ten of teams that have scored in the last nine minutes:")
for sq, goals in secResult.items():
    print(sq + " with " + str(goals) + " goals")

# showing the results of the third part
print("\nPlayers that have scored in at least eight different timedelta:")
for player, goalTime in thResult.items():
    if len(goalTime) > 7:
        for i in range(len(players)):
            if players["wyId"][i] == int(player):
                print(players["shortName"][i])