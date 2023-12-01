import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.Leaderboard
import Database.Category
import Helpers.durations
import Helpers.neatTables

class SweepersCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Sweepers",
                         trigger=["sweepers",],
                         description="See the list of people who have top X",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "cutoff",
            "The X in top X",
            cobble.validations.IsInteger()
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        data = Database.Leaderboard.getSweepers(self.bot.db, argumentValues['cutoff'])



        # Deal with plurality
        if len(data) > 1:
            response = f"There are {len(data)} people"
        else:
            response = f"There is 1 person"

        response += f" with top {argumentValues['cutoff']} in all main categories"

        # If more than 20 people have a sweep, we'll show the top 20 by average rank
        if len(data) > 20:
            response += "\nHere are the 20 with the highest average rank"
            data = data[:19]


        data = [["Player", "Average Rank", "Highest Rank"]]+data
        table = Helpers.neatTables.generateTable([[x[0], str(x[1]), str(x[2])] for x in data])
        response += "```"+table+"```"
        return response
        


        
        
        

        