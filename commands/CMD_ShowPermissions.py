import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Validations.IsName
import Database.User

class ShowPermissionsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Show Permissions",
                         trigger="showperms",
                         description="Display what permissions you (or another user) have",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "user",
            "The name of the person you want to",
            Validations.IsName.IsName(),
            keywordArg=True
        ))

        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if "user" in argumentValues.keys():
            userID = Database.User.identifyUser(self.bot.db, username=argumentValues["user"])
            if userID == None:
                return "User not found!"
            
            userDiscordID = Database.User.User(self.bot.db, userID).getDiscordID()
            if not userDiscordID:
                return "User has not registered with TOL!"
        
        else:
            userDiscordID = messageObject.author.id


        perms = cobble.permissions.getUserPermissions(str(userDiscordID), self.bot.permissionsPath)
        output = "User currently has the permissions:"
        permNames = cobble.permissions.getPermissionNames(self.bot.permissionsPath)
        for perm in perms:
            output += f"\n{permNames[perm]['name']}"

        return output
