import discord

import cobble.command
import cobble.validations
import cobble.permissions

import Database.User
import Database.Run
import Database.Category
import Database.Leaderboard

class DestroyOrphansCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Destroy Orphans",
                         trigger="destroyorphans",
                         description="Remove orphaned leaderboard placements",
                         permission="moderator")
        
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        
        self.bot.db.executeQuery("""
                            DELETE FROM RunCategories
                            WHERE runID NOT IN (SELECT ID FROM Runs)
                            """)
        
        
        Database.Leaderboard.updatePlacements(self.bot.db, [x[0] for x in Database.Category.getCategoryList(self.bot.db, includeExtensions=True)])
        return "Orphans destroyed"