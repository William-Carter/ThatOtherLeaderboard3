import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.Leaderboard
import Database.Category
import Helpers.durations
import Helpers.neatTables
import Validations.IsCategory
import Validations.IsDuration

class WhoHasCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Who Has",
                         trigger=["whohas",],
                         description="See how many (and who) has a certain time or better",
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
        data = self.bot.db.executeQuery(
            """
            SELECT u.Name as name, r.Time
            FROM RunCategories rc
            LEFT JOIN Runs r ON rc.RunID = r.ID
            LEFT JOIN Users u ON r.Runner = u.ID
            WHERE rc.Category = ?
            AND rc.Placement IS NOT NULL
            AND r.Time <= ?
            ORDER BY r.Time
            """,
            (argumentValues['category'], Helpers.durations.seconds(argumentValues['time']))
        )
        
        # Deal with plurality
        if len(data) != 1:
            response = f"There are {len(data)} people"
        else:
            response = f"There is 1 person"

        response += f" with a time of {argumentValues['time']} or better"

        # If more than 20 people have a sweep, we'll show the top 20 by average rank
        if len(data) > 20:
            response += "\nHere are the 20 slowest:"
            data = list(reversed(data))[:19]

        data = [[x[0], Helpers.durations.formatted(x[1])] for x in data]
        data = [["Player", "Time"]]+data
        table = Helpers.neatTables.generateTable(data)
        response += "```"+table+"```"
        return response



        


        
        
        

        