import Database.Interface
import Database.User
import src.DownloadUser
import json
import os
dirPath = os.path.dirname(os.path.realpath(__file__))


def ImportUserInfo(db: Database.Interface.DatabaseInterface):
    for category in ["oob", "inbounds", "unrestricted", "legacy", "glitchless"]:
        print("starting", category)
        with open(dirPath+f"/downloads/{category}DL.json", "r") as f:
            runDL = json.load(f)

        count = 1
        for run in runDL["data"]["runs"]:
            print(count)
            count += 1


            if "id" in run["run"]["players"][0].keys(): # Don't accept src runs from people without an account
                srcPlayerID = run["run"]["players"][0]["id"]

            else:
                continue

            if not Database.User.identifyUser(db, srcID=srcPlayerID):
                userData = src.DownloadUser.DownloadUser(srcPlayerID)
                newUser = Database.User.User(db)

                if userData["data"]["location"]:
                    country = userData["data"]["location"]["country"]["code"]
                else:
                    country = None

                newUser.initialise(
                    userData["data"]["names"]["international"],
                    srcPlayerID,
                    country
                    )
                print(f'Added {userData["data"]["names"]["international"]} from {country}')




        
        

