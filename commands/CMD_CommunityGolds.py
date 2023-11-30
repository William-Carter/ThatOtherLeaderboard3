import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables
import Validations.IsCategory
import Validations.IsGoldsList

class CommunityGoldsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Community Golds",
                         trigger=["cgolds", "comgolds", "commgolds"],
                         description="See the fastest golds from anyone in the community",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "category",
            "The category to see your golds for",
            Validations.IsCategory.IsCategory()
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        
        comgolds = self.bot.db.executeQuery("""
                                        SELECT Maps.LevelName, MIN(Golds.Time), Users.Name
                                        FROM Golds
                                        LEFT JOIN Maps ON Golds.MapName = Maps.Map
                                        LEFT JOIN Users ON Golds.Runner = Users.ID
                                        WHERE Golds.CGEligible = 1
                                        AND Category = ?
                                        GROUP BY Maps.LevelName
                                        ORDER BY Maps.MapOrder
                             """, (argumentValues['category'],))
        


        if len(comgolds) == 0:
            return "No golds have been recorded"
        
        tableData = [["Level", "Time", "Runner"]]
        comsob = 0
        for gold in comgolds:
            comsob += gold[1]
            timeString = Helpers.durations.formatted(gold[1])

            tableData.append([gold[0], timeString, gold[2]])
    
        output = f"{str(argumentValues['category']).capitalize()} community golds:\n```"
        output += Helpers.neatTables.generateTable(tableData)
        output += f"\nCommunity Sum of Best: {Helpers.durations.formatted(comsob)}"
        output += "```"
        return output
