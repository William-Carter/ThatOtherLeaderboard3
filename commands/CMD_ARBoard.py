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

class ARBoardCommand(LeaderboardTemplateCommand):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Average Rank Board",
                         trigger=["arboard",],
                         description="See the leaderboard for average (main category) ranking",
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

        leaderboardData = self.bot.db.executeQuery(""" 
                                SELECT user, avgPlace
                                FROM (
                                    SELECT u.Name as user, COUNT(rc.Placement) as numOfCats, AVG(rc.Placement) as avgPlace
                                    FROM RunCategories rc
                                    LEFT JOIN Runs r ON rc.RunID = r.ID
                                    LEFT JOIN Categories c ON rc.Category = c.ID
                                    LEFT JOIN Users u on r.Runner = u.ID
                                    WHERE c.Extension = 0
                                    GROUP BY r.Runner
                                )
                                WHERE numOfCats = (SELECT COUNT(DISTINCT ID) FROM Categories WHERE extension = 0)
                                ORDER BY avgPlace                                         
                                """)[1:]


        leaderboardData = leaderboardData[start-1:start+19]
        

        leaderboardOutput = self.generateLeaderboard(leaderboardData, offset=start-1)

        # convert all the numerical run lengths to human readable timestrings
        leaderboardOutput = [[x[0], x[1], str(x[2])] for x in leaderboardOutput]

        # Add headers
        leaderboardOutput = [["Place", "Runner", "Average Rank"]]+leaderboardOutput

        return "```"+neatTables.generateTable(leaderboardOutput, padding=2)+"```"