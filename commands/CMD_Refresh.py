import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Database.Leaderboard

import Validations.IsName

import Helpers.durations
import Helpers.neatTables

class RefreshCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Refresh",
                         trigger=["refresh"],
                         description="Refresh leaderboard placements",
                         permission="moderator")
        
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        Database.Leaderboard.updatePlacements(self.bot.db, [x[0] for x in Database.Category.getCategoryList(self.bot.db, includeExtensions=True)])
        return "Leaderboards refreshed"
        
        
        

        