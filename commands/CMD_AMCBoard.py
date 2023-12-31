import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Database.Leaderboard
import Database.User

from commands.LeaderboardTemplate import LeaderboardTemplateCommand
from Helpers import durations
from Helpers import neatTables

class AMCBoardCommand(LeaderboardTemplateCommand):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="AMC Board",
                         trigger=["amcboard", "amc"],
                         description="See the leaderboard for AMC estimates",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "start", 
            "What place to start from", 
            cobble.validations.IsInteger(), 
            True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if 'start' in argumentValues.keys():
            start = int(argumentValues["start"])
        else:
            start = 1

        leaderboardData = Database.Leaderboard.getAMCBoard(self.bot.db)
        leaderboardData = leaderboardData[start-1:start+19]
        

        leaderboardOutput = self.generateLeaderboard(leaderboardData, offset=start-1)

        # convert all the numerical run lengths to human readable timestrings
        leaderboardOutput = [[x[0], x[1], durations.formatted(x[2])] for x in leaderboardOutput]

        # Add headers
        leaderboardOutput = [["Place", "Runner", "AMC Estimate"]]+leaderboardOutput

        return "```"+neatTables.generateTable(leaderboardOutput, padding=2)+"```"