# importing libraries
import json
import pandas as pd
import matplotlib.pyplot as plt

result = {};teamsID = {}

# import and parsing files
teams = open("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\teams.json")
teamsJS = json.loads(teams.read())
matches = pd.read_json("C:\\Users\\asus\\Desktop\\Algoritmic methods for data science\\HM2\\file json\\matches_England.json")

# creating a first step result dictionary
for i in range(len(teamsJS)):
    if (teamsJS[i]["area"]["name"] == "England" or teamsJS[i]["area"]["name"] == "Wales") and teamsJS[i]["type"] != "national":
        result[teamsJS[i]["name"]] = [0]
        teamsID[teamsJS[i]["name"]] = teamsJS[i]["wyId"]

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

# showing the result
plt.xlabel("Num. Giornata")
plt.ylabel("Punti")
for key, values in result.items():
    plt.plot(values, label=key)
plt.legend()
plt.show()

print(result)
