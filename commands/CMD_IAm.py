import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User

class IAmCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="I Am",
                         trigger="iam",
                         description="Tell the bot what your speedrun.com account is",
                         permission="default")
        
        self.addArgument(
            cobble.command.Argument("username",
                                    "Your speedrun.com username",
                                    cobble.validations.IsString()))



    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:

        currentUserID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)

        if currentUserID is not None:
            currentUser = Database.User.User(self.bot.db, currentUserID)
            if currentUser.getName().lower() == argumentValues["username"].lower():
                return "You are already registered as this user."
            
            if not "reregister" in cobble.permissions.getUserPermissions(str(messageObject.author.id), self.bot.permissionsPath):
                return f"You are already registered as {currentUser.getName()} and do not have permission to change your registration! Please contact an administrator if you have an issue."


        userID = Database.User.identifyUser(self.bot.db, username=argumentValues["username"])
        if userID is None:
            return "User not found! Please ensure the relevant speedrun.com account has a fullgame run of Portal submitted."
        
        user = Database.User.User(self.bot.db, userID)

        if user.getDiscordID() is not None:
            return "Someone else is already registered as that player! Please contact an administrator if this is an issue."
        
        user.updateDiscordID(messageObject.author.id)
        return "Accounts successfully linked!"

