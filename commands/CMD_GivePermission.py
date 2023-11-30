import cobble.command
import cobble.validations
import discord

import cobble.permissions

class GivePermissionCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Give Permission",
                         trigger="giveperm",
                         description="Grant a specified permission to a user",
                         permission="admin")
        
        self.addArgument(cobble.command.Argument(
            "userID",
            "The ID (Right Click -> Copy ID) of the user",
            cobble.validations.IsInteger()
        ))
        self.addArgument(cobble.command.Argument(
            "permission",
            "The ID of the permission to grant",
            cobble.validations.IsString()
        ))
        
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:
        # Check the specified permission exists
        if not argumentValues["permission"] in cobble.permissions.getPermissionList(self.bot.permissionsPath):
            return f"Permission {argumentValues['permission']} does not exist!"
    
        # Ensure the user doesn't already have a certain permission
        if argumentValues["permission"] in cobble.permissions.getUserPermissions(argumentValues["userID"], self.bot.permissionsPath):
            return f"User already has permission!"


        cobble.permissions.addUserPermission(argumentValues["userID"], argumentValues["permission"], self.bot.permissionsPath)
        return "Permission granted"

