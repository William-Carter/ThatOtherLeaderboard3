import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.neatTables

class UpdateSetupCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Update setup",
                         trigger=["updatesetup", "us"],
                         description="Update your setup",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "element",
            "The element to update. Currently supported are: dpi, sensitivity, hz, mouse and keyboard",
            cobble.validations.IsString()
        ))
        self.addArgument(cobble.command.Argument(
            "value",
            "The value to set it to",
            cobble.validations.IsString(),
            caseSensitive=True
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        runnerID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
        if not runnerID:
            return "User is not registered!"
        
        argumentValues['element'] = argumentValues['element'].lower()
        elementInfo = self.bot.db.executeQuery("""
                                          SELECT Name, Type
                                          FROM SetupElements
                                          WHERE ID = ?
                                          """, (argumentValues['element'],))
        if len(elementInfo) == 0:
            return f"Invalid element \"{argumentValues['setup']}\""
        
        elementInfo = elementInfo[0]
        if elementInfo[1] == "num":
            if not cobble.validations.IsNumber.validate("", argumentValues['value']):
                return "Invalid value! Must be a number"


            self.bot.db.executeQuery("""
                                INSERT OR REPLACE INTO UserSetups (UserID, SetupElement, SetupNum)
                                VALUES (?, ?, ?)
                                """, (runnerID, argumentValues['element'], argumentValues['value']))
            
        elif elementInfo[1] == "string":
            if not cobble.validations.IsString.validate("", argumentValues['value']):
                return "Invalid value! Must be a valid string!"


            self.bot.db.executeQuery("""
                                INSERT OR REPLACE INTO UserSetups (UserID, SetupElement, SetupValue)
                                VALUES (?, ?, ?)
                                """, (runnerID, argumentValues['element'], argumentValues['value']))
            

        return "Setup updated."

