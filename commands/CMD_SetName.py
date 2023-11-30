import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category

import Validations.IsName

import Helpers.durations
import Helpers.neatTables

class SetNameCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Set Name",
                         trigger=["setname", "sn"],
                         description="Change the name TOL knows you by",
                         permission="changename")
        
        self.addArgument(cobble.command.Argument(
            "name",
            "The new name you want to use",
            Validations.IsName.IsName(),
            caseSensitive=True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if Database.User.identifyUser(self.bot.db, username=argumentValues["name"]):
            return "That name is already in use!"
        
        user = Database.User.User(self.bot.db, userID=Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id))
        user.setName(argumentValues["name"])

        return "Name updated."
        
        
        

        