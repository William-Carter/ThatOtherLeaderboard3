import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Database.Leaderboard
import Database.RegionalBoards


import Validations.IsCategory

from commands.LeaderboardTemplate import LeaderboardTemplateCommand
from Helpers import durations
from Helpers import neatTables

class GoldBoardCommand(LeaderboardTemplateCommand):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Gold Leaderboard",
                         trigger=["goldboard", "gb"],
                         description="See the leaderboard for a specific gold or sum of best",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category that you want to see the leaderboard for",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "level", 
            "What level to check golds for. Leave blank to see sum of best leaderboard.", 
            cobble.validations.IsString(), 
            True
        ))
        self.addArgument(cobble.command.Argument(
            "start", 
            "What place to start from", 
            cobble.validations.IsInteger(), 
            True
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:

        if 'level' in argumentValues.keys():
            mapName = self.bot.db.getSingle("""
                                SELECT Map
                                FROM Maps
                                WHERE Advanced = 0
                                AND LevelName = ?
                                ORDER BY MapOrder
                             """, (argumentValues['level'],))

            if not mapName:
                return "Level does not exist"


            leaderboardData = self.bot.db.executeQuery("""
                                                    SELECT Users.Name, Golds.Time
                                                    FROM Golds
                                                    LEFT JOIN Users ON Golds.Runner = Users.ID
                                                    WHERE MapName = ?
                                                    AND Category = ?
                                                    AND CGEligible = 1
                                                    ORDER BY Golds.Time
                                                    """, (mapName, argumentValues['category']))
            
            header = f"Gold Leaderboard for {argumentValues['category']} {argumentValues['level']}:\n"
            
        else:
            leaderboardData = self.bot.db.executeQuery("""
                                                    SELECT Users.Name, SUM(Golds.time)
                                                    FROM Golds
                                                    LEFT JOIN Users ON Golds.Runner = Users.ID
                                                    WHERE Category = ?
                                                    GROUP BY Users.Name
                                                    ORDER BY SUM(Golds.Time)
                                                    """, (argumentValues['category'], ))
            header = "Sum of Best Leaderboard:\n"

        if 'start' in argumentValues.keys():
            start = int(argumentValues["start"])
        else:
            start = 1

        leaderboardData = leaderboardData[start-1:min(len(leaderboardData), start+19)]

        #filteredLeaderboard = [[x[2], x[3]] for x in leaderboardData] # extracts just name and time
        leaderboardOutput = self.generateLeaderboard(leaderboardData, offset=start-1)

        # convert all the numerical run lengths to human readable timestrings
        leaderboardOutput = [[x[0], x[1], durations.formatted(x[2])] for x in leaderboardOutput]

        # Add headers
        leaderboardOutput = [["Place", "Runner", "Time"]]+leaderboardOutput

        return header+"```"+neatTables.generateTable(leaderboardOutput, padding=2)+"```"