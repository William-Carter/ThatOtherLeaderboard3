import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Database.Leaderboard
import Database.SCKR


import Validations.IsCategory

from commands.LeaderboardTemplate import LeaderboardTemplateCommand
from Helpers import durations
from Helpers import neatTables

class SCKRCommand(LeaderboardTemplateCommand):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="SCKR Leaderboard",
                         trigger=["sckrboard", "sckr"],
                         description="See the SCKR leaderboard",
                         permission="default")
        

        self.addArgument(cobble.command.Argument(
            "start", 
            "What place to start from", 
            cobble.validations.IsInteger(), 
            True
        ))
        self.addArgument(cobble.command.Argument(
            "country",
            "Filter the leaderboard to a single country",
            cobble.validations.IsString(),
            True
        ))
        self.addArgument(cobble.command.Argument(
            "continent",
            "Filter the leaderboard to a single continent",
            cobble.validations.IsString(),
            True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:

        if 'country' in argumentValues.keys():
            leaderboardData, countryName = Database.SCKR.getSCKRBoard(self.bot.db, country=argumentValues['country'])
            if countryName == "invalid":
                return "Invalid country!"
            if not leaderboardData:
                return "No runs found!"
            header = f"Leaderboard for {countryName}:\n"

        elif 'continent' in argumentValues.keys():
            leaderboardData, continentName = Database.SCKR.getSCKRBoard(self.bot.db, continent=argumentValues['continent'])
            if continentName == "invalid":
                return "Invalid continent!"
            if not leaderboardData:
                return "No runs found!"
            header = f"Leaderboard for {continentName}:\n"




            
        else:
            leaderboardData = Database.SCKR.getSCKRBoard(self.bot.db)[0]
            header = "Global Leaderboard:\n"

        if 'start' in argumentValues.keys():
            start = int(argumentValues["start"])
        else:
            start = 1

        leaderboardData = leaderboardData[start-1:min(len(leaderboardData)-1, start+19)]


        if 'continent' in argumentValues.keys():
            leaderboardOutput = self.generateLeaderboard(leaderboardData, key=1, offset=start-1)

            # convert all the numerical run lengths to human readable timestrings
            leaderboardOutput = [[x[0], x[1], str(x[2]), str(x[3]).title()] for x in leaderboardOutput]

            # Add headers
            leaderboardOutput = [["Place", "Runner", "SCKR", "Country"]]+leaderboardOutput
        else:    
            leaderboardOutput = self.generateLeaderboard(leaderboardData, key=1, offset=start-1)

            # convert all the numerical run lengths to human readable timestrings
            leaderboardOutput = [[x[0], x[1], str(x[2])] for x in leaderboardOutput]

            # Add headers
            leaderboardOutput = [["Place", "Runner", "SCKR"]]+leaderboardOutput

        return header+"```"+neatTables.generateTable(leaderboardOutput, padding=2)+"```"