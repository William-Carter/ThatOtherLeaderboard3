import cobble.command
import cobble.validations
import discord

class LeaderboardTemplateCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot, name: str, trigger: str, description: str, permission: str = "default"):
        """
        A template for commands that display a leaderboard of some description.
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name=name,
                         trigger=trigger,
                         description=description,
                         permission=permission)
        
    def generateLeaderboard(self, data: list[list[any]], key: int = -1, offset: int = 0) -> list[list[str]]:
        """
        Constructs a leaderboard from a list of values

        Parameters:
            data - an already-sorted list of lists

            key - which index the list is sorted by, default is -1

        """

        output = []

        previousValue = None
        place = offset
        displayedPlace = place
        for row in data:
            place += 1
            if row[key] != previousValue:
                displayedPlace = place 
                previousValue = row[key]

            output.append([str(displayedPlace)+".",]+list(row))

        return output


        
    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> str:
        return None