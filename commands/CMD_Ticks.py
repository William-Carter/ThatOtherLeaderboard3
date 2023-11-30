import cobble.command
import cobble.validations
import discord

import Validations.IsDuration
import Helpers.durations

class TicksCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Ticks",
                         trigger=["ticks",],
                         description="Convert a time to ticks",
                         permission="default")
        self.addArgument(cobble.command.Argument("time", "The duration you want to convert", Validations.IsDuration.IsDuration()))
    
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:

        timeString = argumentValues["time"]
        timeNum = Helpers.durations.seconds(timeString)
        roundedTimeNum = Helpers.durations.correctToTick(timeNum)
        roundedTimeString = Helpers.durations.formatted(roundedTimeNum)
        rounded = not (timeNum == roundedTimeNum)
        ticks = int(round(roundedTimeNum/0.015, 0))
        return f"Had to round: {rounded}\nTime: {roundedTimeString}\nTicks: {ticks}"