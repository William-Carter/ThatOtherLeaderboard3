import cobble.command
import cobble.validations
import discord

import Validations.IsDuration
import Helpers.durations

class SecondsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Seconds",
                         trigger=["seconds", "secs", "sex"],
                         description="Convert a number of ticks to seconds",
                         permission="default")
        self.addArgument(cobble.command.Argument("ticks", "The duration you want to convert", cobble.validations.IsInteger()))
    
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:


        time = Helpers.durations.formatted(round(int(argumentValues["ticks"])*0.015, 3))
        return f"{argumentValues['ticks']} ticks is {time}"