import requests
import json
import os
dirPath = os.path.dirname(os.path.realpath(__file__))


portalID = "4pd0n31e"

noslaID = "n2yq98ko"
inboundsID = "7wkp6v2r"
oobID = "lvdowokp"
glitchlessID = "wk6pexd1"

legUnVar = "ql61qmv8"
unresVal = "21g5r9xl"
legacyVal = "jqz97g41"

def getRuns() -> None:
    """
    Requests the leaderboard for each category and dumps it to a json file.
    Will place 5 json files in the program directory.
    """
    print("Getting inbounds leaderboard")
    inboundsLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{inboundsID}").text
    with open(dirPath+"/downloads/inboundsDL.json", "w") as f:
        f.write(inboundsLB)


    print("Getting oob leaderboard")
    oobLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{oobID}").json()
    with open(dirPath+"/downloads/oobDL.json", "w") as f:
        json.dump(oobLB, f)

    print("Getting glitchless leaderboard")
    glitchlessLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{glitchlessID}").json()
    with open(dirPath+"/downloads/glitchlessDL.json", "w") as f:
        json.dump(glitchlessLB, f)

    print("Getting legacy leaderboard")
    legacyLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{noslaID}?var-{legUnVar}={legacyVal}").json()
    with open(dirPath+"/downloads/legacyDL.json", "w") as f:
        json.dump(legacyLB, f)

    print("Getting unrestricted leaderboard")
    unrestrictedLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{noslaID}?var-{legUnVar}={unresVal}").json()
    with open(dirPath+"/downloads/unrestrictedDL.json", "w") as f:
        json.dump(unrestrictedLB, f)

if __name__ == "__main__":
    getRuns()
