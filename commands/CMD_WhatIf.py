import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.Category
import Helpers.durations
import Helpers.neatTables
import Validations.IsCategory
import Validations.IsDuration

class WhatIfCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="What If",
                         trigger=["whatif",],
                         description="See what rank a certain time would be",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "Which category to check for times in",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "time",
            "What time to check for",
            Validations.IsDuration.IsDuration()
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        duration = Helpers.durations.correctToTick(Helpers.durations.seconds(argumentValues['time']))
        data = self.bot.db.executeQuery(
            """
            SELECT COUNT(r.ID), c.Name
            FROM RunCategories rc
            LEFT JOIN Runs r on rc.RunID = r.ID
            LEFT JOIN Categories c on rc.Category = c.ID
            WHERE rc.Placement IS NOT NULL
            AND rc.Category = ?
            AND r.Time < ?
            """,
            (argumentValues['category'], duration))[0]
        count = data[0]
        catName = data[1]

        return f"A time of {Helpers.durations.formatted(duration)} would place {Helpers.durations.formatLeaderBoardPosition(count+1)} on the {catName} leaderboard"





        


        
        
        

        