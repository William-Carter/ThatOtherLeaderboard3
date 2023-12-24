import discord
import datetime

import cobble.command
import cobble.validations
import cobble.permissions

import Database.User
import Database.Run
import Database.Category
import Database.Leaderboard
import Validations.IsDuration

class DeleteCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Delete",
                         trigger="delete",
                         description="Delete a run given the ID",
                         permission="moderator")
        
        self.addArgument(cobble.command.Argument(
            "id",
            "The id of the run",
            cobble.validations.IsInteger()
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        
        self.bot.db.executeQuery("""
                            DELETE FROM Runs
                            WHERE ID = ?
                            """, (int(argumentValues['id']),))
        
        self.bot.db.executeQuery("""
                            DELETE FROM RunCategories
                            WHERE RunID = ?
                            """, (int(argumentValues['id']),))
        Database.Leaderboard.updatePlacements(self.bot.db)
        return "Run deleted."