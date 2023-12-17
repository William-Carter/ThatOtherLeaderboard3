import Database.Interface
import Database.User
import Database.Run
import Database.Leaderboard
import Helpers.durations
import json
import os
dirPath = os.path.dirname(os.path.realpath(__file__))


def ImportRunInfo(db: Database.Interface.DatabaseInterface):
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


            userID = Database.User.identifyUser(db, srcID=srcPlayerID)
            if not userID:
                print("User missing, aborting run insertion")
                continue

            runner = Database.User.User(db, userID)

            time = Helpers.durations.correctToTick(run["run"]["times"]["primary_t"])

            if Database.Run.runExists(db, userID, category, time):
                continue

            date = run["run"]["date"]
            newRun = Database.Run.Run(db)
            newRun.initialize(userID, time, category, date)
            print(f"Added a(n) {category} time of {Helpers.durations.formatted(time)} by {runner.getName()}")


        Database.Leaderboard.updatePlacements(db, [category,])

        
        

