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

class CommunityGoldEligibilityCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Community Gold Eligibility",
                         trigger=["eligible", "cgeligible"],
                         description="Toggle whether one of your golds counts towards the community sum of best",
                         permission="updategolds")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category to update",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "level",
            "The level you want to update (02/03, 15, e01, etc)",
            cobble.validations.IsString()
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        runnerID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
        if not runnerID:
            return "User is not registered!"
        


        mapName = self.bot.db.getSingle("""
                                SELECT Map
                                FROM Maps
                                WHERE Advanced = 0
                                AND LevelName = ?
                                ORDER BY MapOrder
                             """, (argumentValues['level'],))

        if not mapName:
            return "Level does not exist"
        

        self.bot.db.executeQuery("""
                                 UPDATE Golds
                                 SET CGEligible = 1-CGEligible
                                 WHERE Category = ?
                                 AND Runner = ?
                                 AND MapName = ?
                                 """, (argumentValues['category'], runnerID, mapName))
        
        newValue = self.bot.db.getSingle("""
                                SELECT CGEligible
                                FROM Golds
                                WHERE Category = ?
                                AND Runner = ?
                                AND MapName = ?
                                """, (argumentValues['category'], runnerID, mapName))
        
        if newValue:
            return f"Your gold for {argumentValues['category']} {argumentValues['level']} is now eligible for the community gold"
        
        else:
            return f"Your gold for {argumentValues['category']} {argumentValues['level']} is no longer eligible for the community gold"
        

        


        
