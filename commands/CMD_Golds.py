import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables
import Validations.IsCategory
import Validations.IsGoldsList

class GoldsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Golds",
                         trigger=["golds",],
                         description="See your (or someone else's) golds for a category",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category to see your golds for",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "user",
            "The person whose golds you want to see",
            cobble.validations.IsString(),
            keywordArg=True
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if 'user' in argumentValues.keys():
            runnerID = Database.User.identifyUser(self.bot.db, username=argumentValues['user'])
            if not runnerID:
                return "No user with that name!"
            
        else:
            runnerID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
            if not runnerID:
                return "User is not registered!"
            
        runner = Database.User.User(self.bot.db, runnerID)
        
        golds = runner.getGolds(argumentValues['category'])
        


        if len(golds) == 0:
            return "User hasn't recorded any golds!"
        
        hasIneligibleGolds = False
        tableData = [["Level", "Time"]]
        sob = 0
        for gold in golds:
            sob += gold[1]
            timeString = Helpers.durations.formatted(gold[1])
            if not gold[2]:
                timeString += "*"
                hasIneligibleGolds = True

            tableData.append([gold[0], timeString])

        output = f"{runner.name}'s {argumentValues['category']} golds:\n```"
        output += Helpers.neatTables.generateTable(tableData)
        output += f"\nSum of Best: {Helpers.durations.formatted(sob)}"
        output += "```"

        if hasIneligibleGolds:
            output += "\nTimes with asterisks* are ineligible for comgold due to strat differences"
        return output
