import discord
import datetime

import cobble.command
import cobble.validations
import cobble.permissions

import Database.User
import Database.Run
import Database.Category
import Database.Leaderboard
import Validations.IsCategory
import Validations.IsDuration
import Validations.IsName
import Helpers.durations

class SubmitForCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Submit For",
                         trigger="submitfor",
                         description="Submit a run to the leaderboard on behalf of another runner",
                         permission="moderator")
        
        self.addArgument(cobble.command.Argument(
            "user",
            "The user whose run you are submitting",
            Validations.IsName.IsName()
        ))
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category of the run",
            Validations.IsCategory.IsCategory()
        ))
        self.addArgument(cobble.command.Argument(
            "time",
            "The duration of the run",
            Validations.IsDuration.IsDuration()
        ))
        self.addArgument(cobble.command.Argument(
            "date",
            "The date the run was performed, in the format YYYY-MM-DD",
            cobble.validations.IsISO8601(),
            keywordArg=True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        userID = Database.User.identifyUser(self.bot.db, username=argumentValues["user"])
        if not userID:
            return f"No user with name {argumentValues['user']}"

        player = Database.User.User(self.bot.db, userID)
        runTime = Helpers.durations.seconds(argumentValues['time'])
        runTime = Helpers.durations.correctToTick(runTime)


        # If no date is provided, we just assume it was performed today
        if 'date' in argumentValues:
            date = argumentValues['date']
        else:
            date = datetime.date.today().strftime("%Y-%m-%d")

        player.addRun(argumentValues['category'], runTime, date)
        Database.Leaderboard.updatePlacements(self.bot.db)
        return f"Submitted a time of {Helpers.durations.formatted(runTime)} to {argumentValues['category']} on behalf of {player.name}"
