import cobble.command
import cobble.validations
import discord

import cobble.permissions

class RemovePermissionCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Revoke Permission",
                         trigger="takeperm",
                         description="Revoke a specified perm from a user",
                         permission="admin")
        
        self.addArgument(cobble.command.Argument(
            "userID",
            "The ID (Right Click -> Copy ID) of the user",
            cobble.validations.IsInteger()
        ))
        self.addArgument(cobble.command.Argument(
            "permission",
            "The ID of the permission to revoke",
            cobble.validations.IsString()
        ))
        
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:
        # Check the specified permission exists
        if not argumentValues["permission"] in cobble.permissions.getPermissionList(self.bot.permissionsPath):
            return f"Permission {argumentValues['permission']} does not exist!"
    
        # Ensure the user has the permission
        if not argumentValues["permission"] in cobble.permissions.getUserPermissions(argumentValues["userID"], self.bot.permissionsPath):
            return f"User doesn't have specified permission!"


        cobble.permissions.removeUserPermission(argumentValues["userID"], argumentValues["permission"], self.bot.permissionsPath)
        return "Permission revoked"

