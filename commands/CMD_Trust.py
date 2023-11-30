import cobble.command
import cobble.validations
import discord

import cobble.permissions

class TrustCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Trust",
                         trigger="trust",
                         description="Trust a user",
                         permission="truster")
        
        self.addArgument(cobble.command.Argument(
            "userID",
            "The ID (Right Click -> Copy ID) of the user",
            cobble.validations.IsInteger()
        ))
        
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:

        trustedPermissions = [
            "submit",
            "updategolds",
            "changename"
        ]
            
    
        for permission in trustedPermissions:
            if permission in cobble.permissions.getUserPermissions(argumentValues["userID"], self.bot.permissionsPath):
                continue


            cobble.permissions.addUserPermission(argumentValues["userID"], permission, self.bot.permissionsPath)
        return "User is now trusted!"