import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables

class RunsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Runs",
                         trigger=["runs"],
                         description="See your (or another person's) submitted runs",
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
        runs = user.getRuns()
        output = f"Runs for {user.name}"
        tableData = [["ID", "Category", "Time", "Date"]]
        for run in runs:
            tableData.append([str(run[0]), run[1], Helpers.durations.formatted(run[2]), run[3]])

        output += "\n```"+Helpers.neatTables.generateTable(tableData)+"```"
        return output
        
        
        
        

        