import cobble.command
import discord
import sys

class EmergencyStopCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Emergency Stop",
                         trigger=["stop", "emergencystop"],
                         description="Suspend the bot",
                         permission="moderator")
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        sys.exit()
        

        