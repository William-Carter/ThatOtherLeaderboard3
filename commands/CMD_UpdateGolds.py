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

class UpdateGoldsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Update golds",
                         trigger=["updategolds", "ug"],
                         description="Update your golds for a category",
                         permission="updategolds")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category to update your golds for",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "times",
            "The times for all your golds, pasted in from livesplit",
            Validations.IsGoldsList.IsGoldsList()
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        runnerID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
        if not runnerID:
            return "User is not registered!"
        
        times = [Helpers.durations.correctToTick(Helpers.durations.seconds(x)) for x in argumentValues['times'].split("\n")]

        user = Database.User.User(self.bot.db, runnerID)

        sob = user.updateGolds(argumentValues['category'], times)
    
        
        return f"Golds updated. Your new sum of best is {Helpers.durations.formatted(sob)}"
