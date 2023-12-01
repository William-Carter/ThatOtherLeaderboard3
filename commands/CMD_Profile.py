import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables

class ProfileCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Profile",
                         trigger=["profile", "pf"],
                         description="See your (or another person's) profile",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "player",
            "The name of the player",
            cobble.validations.IsString(),
            keywordArg=True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if "player" in argumentValues.keys():
            userID = Database.User.identifyUser(self.bot.db, username=argumentValues["player"])
            if userID == None:
                return "User not found!"
        else:
            userID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
            if userID == None:
                return "No data for user. Please link your discord with your speedrun.com account using the `.iam` command"
            

        user = Database.User.User(self.bot.db, userID)

        pbs = user.getPersonalBests()
        pbs = sorted(pbs, key= lambda x: x[1])

        
        output = f"Profile for {user.getName()}:\n```"
        tableData = [["Category", "Time", "Place"]]
        for pb in pbs:
            if not pb[2]:
                tableData.append([Database.Category.getCategoryName(self.bot.db, pb[1]), Helpers.durations.formatted(pb[3]), Helpers.durations.formatLeaderBoardPosition(pb[4])])


        
        output += Helpers.neatTables.generateTable(tableData)
        amcEstimate = user.getAMCEstimate()
        if amcEstimate:
            output += f"\nAMC Estimate: {Helpers.durations.formatted(amcEstimate)}"


        output += f"\nAverage Rank: {user.getAverageRank()}"
        output += f"\n\nRepresenting {str(user.getCountry()[1]).title()}```"
        return output

        
        
        

        