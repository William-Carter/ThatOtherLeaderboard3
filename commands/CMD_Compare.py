import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables
import Validations.IsName
import Validations.IsGoldsList


class CompareCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Compare",
                         trigger=["compare",],
                         description="Compare two runners",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "comparison",
            "What it is you want to compare",
            IsComparison()
        ))
        self.addArgument(cobble.command.Argument(
            "person1",
            "The first of the two people to be compared",
            Validations.IsName.IsName(),
            keywordArg=True
        ))
        self.addArgument(cobble.command.Argument(
            "person2",
            "The second of the two people to be compared",
            Validations.IsName.IsName(),
            keywordArg=True
        )) 

        self.addArgument(cobble.command.Argument(
            "category",
            "The category to compare under, where applicable",
            Validations.IsName.IsName(),
            keywordArg=True
        )) 
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        match argumentValues["comparison"]:
            case "pbs":
                return await self.pbCompare(messageObject, argumentValues)
            case "golds":
                return await self.goldCompare(messageObject, argumentValues)
            case "comgolds":
                return await self.comgoldCompare(messageObject, argumentValues)



    async def pbCompare(self, messageObject: discord.message.Message, argumentValues: dict):
        pattern = self.generatePersonPattern(argumentValues)
        if pattern[2] == "1":
            return "Comparing pbs doesn't require a supplied category!"
        match pattern:
            case "000":
                return "At least one person is needed to compare against!"
            case "100": # Compare self to person 1
                user1id = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
                if not user1id:
                    return "You aren't registered with TOL!"
                user1 = Database.User.User(self.bot.db, userID=user1id)

                user2id = Database.User.identifyUser(self.bot.db, username=argumentValues["person1"])
                if not user2id:
                    return f"No user with name {argumentValues['person1']}!"
                user2 = Database.User.User(self.bot.db, userID=user2id)


            case "110": # Compare person 1 to person 2
                user1id = Database.User.identifyUser(self.bot.db, username=argumentValues["person1"])
                if not user1id:
                    return f"No user with name {argumentValues['person1']}!"
                user1 = Database.User.User(self.bot.db, userID=user1id)
                
                user2id = Database.User.identifyUser(self.bot.db, username=argumentValues["person2"])
                if not user2id:
                    return f"No user with name {argumentValues['person2']}!"
                user2 = Database.User.User(self.bot.db, userID=user2id)



        user1pbs = user1.getPersonalBests()
        user2pbs = user2.getPersonalBests()
        categories = Database.Category.getCategoryList(self.bot.db)
        usedCategories = []
        for category in categories:
            if category[0] in [x[1] for x in user1pbs] or category in [x[1] for x in user2pbs]:
                usedCategories.append(category)

        tableData = []

        header = ["Category"]
        for category in usedCategories:
            header.append(category[1])

        header += ["", "Avg. Rank"]


        tableData.append(header)
        tableData.append(["" for i in range(len(usedCategories)+3)])

        user1times = [user1.name]
        user1ranks = [""]
        user1pbdict = {}
        for category in usedCategories:
            PB = ""
            rank = ""
            for run in user1pbs:
                if run[1] == category[0]:
                    PB = Helpers.durations.formatted(run[3])
                    rank = Helpers.durations.formatLeaderBoardPosition(run[4])
                    user1pbdict[category[0]] = {"time": run[3], "rank": run[4]}

            user1times.append(PB)
            user1ranks.append(rank)


        user1averageRank = user1.getAverageRank()
        user1times += ["", str(user1averageRank) if user1averageRank else ""]
        user1ranks += ["", ""]

        tableData.append(user1times)
        tableData.append(user1ranks)
        tableData.append(["" for i in range(len(usedCategories)+3)])



        user2times = [user2.name]
        user2ranks = [""]
        for category in usedCategories:
            PB = ""
            rank = ""
            for run in user2pbs:
                if run[1] == category[0]:
                    PB = Helpers.durations.formatted(run[3])
                    rank = Helpers.durations.formatLeaderBoardPosition(run[4])
                    if category[0] in user1pbdict.keys():
                        timeDiff = run[3] - user1pbdict[category[0]]["time"]
                        rankDiff = run[4] - user1pbdict[category[0]]["rank"]
                        PB += f" ({('+' if timeDiff>=0 else '-')+Helpers.durations.formatted(abs(timeDiff))})"
                        rank += f" ({('+' if rankDiff>=0 else '-')+str(abs(rankDiff))})"

            user2times.append(PB)
            user2ranks.append(rank)

        
        averageRank = user2.getAverageRank()
        avgRankString = str(averageRank) if averageRank else ""
        rankDiff = averageRank-user1averageRank
        if user1averageRank:
            avgRankString += f" ({('+' if rankDiff>=0 else '-')+str(abs(rankDiff))})"
        user2times += ["", avgRankString]
        user2ranks += ["", ""]


        tableData.append(user2times)
        tableData.append(user2ranks)





        tableData = [list(reversed(x)) for x in list(zip(*tableData[::-1]))]
        table = Helpers.neatTables.generateTable(tableData, padding=2)
        table = "```"+table+"```"

        return table

        
    async def goldCompare(self, messageObject: discord.message.Message, argumentValues: dict):
        pattern = self.generatePersonPattern(argumentValues)
        if pattern[2] == "0":
            return "Comparing golds requires category=!"
        match pattern:
            case "001":
                return "At least one person is needed to compare against!"
            case "101": # Compare self to person 1
                user1id = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
                if not user1id:
                    return "You aren't registered with TOL!"
                user1 = Database.User.User(self.bot.db, userID=user1id)

                user2id = Database.User.identifyUser(self.bot.db, username=argumentValues["person1"])
                if not user2id:
                    return f"No user with name {argumentValues['person1']}!"
                user2 = Database.User.User(self.bot.db, userID=user2id)


            case "111": # Compare person 1 to person 2
                user1id = Database.User.identifyUser(self.bot.db, username=argumentValues["person1"])
                if not user1id:
                    return f"No user with name {argumentValues['person1']}!"
                user1 = Database.User.User(self.bot.db, userID=user1id)
                
                user2id = Database.User.identifyUser(self.bot.db, username=argumentValues["person2"])
                if not user2id:
                    return f"No user with name {argumentValues['person2']}!"
                user2 = Database.User.User(self.bot.db, userID=user2id)

        userGolds = []
        for user in [user1, user2]:
            golds = user.getGolds(argumentValues['category'])
            if len(golds) == 0:
                return f"User {user.name} doesn't have any recorded golds!"
            userGolds.append({x[0]: [x[1], x[2]] for x in golds})


        maps = self.bot.db.executeQuery("""
                            SELECT Map, LevelName
                            FROM Maps
                            WHERE Advanced = 0
                            ORDER BY MapOrder
                            """)

        tableData = [["Map", user1.name, user2.name]]
        for map in maps:
            # I am using the level name (00/01) as the key here and I hate it but I'm too lazy to fix it rn
            goldDifference = round(userGolds[1][map[1]][0]-userGolds[0][map[1]][0], 3)
            goldDifference = " ("+("+" if (goldDifference >= 0) else "-")+Helpers.durations.formatted(abs(goldDifference))+")"
            user1gold = Helpers.durations.formatted(userGolds[0][map[1]][0]) 
            user2gold = Helpers.durations.formatted(userGolds[1][map[1]][0])+goldDifference
            tableData.append([map[1], user1gold, user2gold])


        user1sob = sum([x[1] for x in user1.getGolds(argumentValues['category'])])
        user2sob = sum([x[1] for x in user2.getGolds(argumentValues['category'])])
        sobDifference = round(user2sob-user1sob, 3)
        sobDifference = " ("+("+" if (sobDifference >= 0) else "-")+Helpers.durations.formatted(abs(sobDifference))+")"

        tableData.append(["", "", ""])
        tableData.append(["Total", Helpers.durations.formatted(user1sob), Helpers.durations.formatted(user2sob)+sobDifference])

        header = f"Comparing {Database.Category.getCategoryName(self.bot.db, argumentValues['category'])} golds for {user1.name} and {user2.name}"
        return header+"\n```"+Helpers.neatTables.generateTable(tableData)+"```"


    async def comgoldCompare(self, messageObject: discord.message.Message, argumentValues: dict):
        pattern = self.generatePersonPattern(argumentValues)
        if pattern[2] == "0":
            return "Comparing to comgolds requires category=!"
        match pattern:
            case "001":
                userid = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
                if not userid:
                    return "You aren't registered with TOL!"
            case "101": # Compare self to person 1
                userid = Database.User.identifyUser(self.bot.db, username=argumentValues["person1"])
                if not userid:
                    return f"No user with name {argumentValues['person1']}!"


            case "111": # Compare person 1 to person 2
                return "Only one person can be compared to comgolds at a time!"
            


        user = Database.User.User(self.bot.db, userid)
        userGolds = user.getGolds(argumentValues['category'])
        # This query is a copy paste from the comgold command, consolidate them later you twit
        comgolds = self.bot.db.executeQuery("""
                                        SELECT Maps.LevelName, MIN(Golds.Time), Users.Name
                                        FROM Golds
                                        LEFT JOIN Maps ON Golds.MapName = Maps.Map
                                        LEFT JOIN Users ON Golds.Runner = Users.ID
                                        WHERE Golds.CGEligible = 1
                                        AND Category = ?
                                        GROUP BY Maps.LevelName
                                        ORDER BY Maps.MapOrder
                             """, (argumentValues['category'],))
        
        tableData = [["Level", "Comgold", user.name]]
        userSob = 0
        comSob = 0
        
        for index, gold in enumerate(userGolds):
            # I am praying that things are always sorted fine. It think they should be, but who knows
            comgoldTime = comgolds[index][1]
            comSob += comgoldTime
            userGold = gold[1]
            userSob += userGold
            difference = userGold-comgoldTime

            comgoldTime = Helpers.durations.formatted(comgoldTime)
            userGold = Helpers.durations.formatted(userGold)
            difference = " ("+("+" if (difference >= 0) else "-")+Helpers.durations.formatted(abs(difference))+")"

            tableData.append([gold[0], comgoldTime, userGold+difference])



        sobDifference = userSob-comSob
        sobDifference = " ("+("+" if (sobDifference >= 0) else "-")+Helpers.durations.formatted(abs(sobDifference))+")"
        tableData.append(["", "", ""])
        tableData.append(["Total", Helpers.durations.formatted(comSob), Helpers.durations.formatted(userSob)+sobDifference])
        header = f"Comparing against {Database.Category.getCategoryName(self.bot.db, argumentValues['category'])} comgolds for {user.name}"
        return header+"\n```"+Helpers.neatTables.generateTable(tableData)+"```"

        

    def generatePersonPattern(self, argumentValues: dict) -> str:
        pattern = list("000")
        if "person1" in argumentValues.keys():
            pattern[0] = "1"
        if "person2" in argumentValues.keys():
            pattern[1] = "1"
        if "category" in argumentValues.keys():
            pattern[2] = "1"

        return "".join(pattern)

class IsComparison(cobble.validations.Validation):
        def __init__(self):
            super().__init__()
            self.requirements = "Must be one of: pbs, golds, comgolds"

        def validate(self, x: str) -> bool:
            """
            Evaluates a given string to see if it can be parsed into a number of seconds
            Parameters:
                x - The string to be tested
            Returns:
                valid - Whether the string was successfully parsed
            """
            return (x.lower() in ["pbs", "golds", "comgolds"])