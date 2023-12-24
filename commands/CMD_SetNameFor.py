import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category

import Validations.IsName

import Helpers.durations
import Helpers.neatTables

class SetNameForCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Set Name For",
                         trigger=["setnamefor"],
                         description="Change another person's name",
                         permission="moderator")
        
        self.addArgument(cobble.command.Argument(
            "user",
            "The user whose name you are changing",
            Validations.IsName.IsName()
        ))
        
        self.addArgument(cobble.command.Argument(
            "name",
            "The new name you want to use",
            Validations.IsName.IsName(),
            caseSensitive=True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        userID = Database.User.identifyUser(self.bot.db, username=argumentValues["user"])
        if not userID:
            return f"No user with name {argumentValues['user']}"

        user = Database.User.User(self.bot.db, userID)

        if Database.User.identifyUser(self.bot.db, username=argumentValues["name"]):
            return "That name is already in use!"
        
        
        
        user.setName(argumentValues["name"])

        return "Name updated."
        
        
        

        