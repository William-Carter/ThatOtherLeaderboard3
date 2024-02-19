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

class RecordsCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Records",
                         trigger=["records",],
                         description="See the current records in all categories",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "region",
            "The region (continent or country) that you want to see records for",
            cobble.validations.IsString(),
            keywordArg=True
        ))
        self.addArgument(cobble.command.Argument(
            "includeExtensions",
            "Whether you want to include category extensions in the result",
            cobble.validations.IsBool(),
            keywordArg=True
        ))
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        regionFilter = ""

        regionName = "World"
        includeExtensions = 0
        ## Step 1 - check if region provided is a continent (query for list of continents and check if input is in list)
        ## Step 2 - if it is, set regionfilter accordingly with the continent code
        ## Step 3 - if it isn't, repeat the same process for country
        ## Step 4 - if neither check passes, return an 'invalid region' message
        if "region" in argumentValues.keys():
            continents = self.bot.db.executeQuery("SELECT ID, Name, Descriptor FROM Continents")
            for continent in continents:
                if argumentValues["region"].lower() == continent[1].lower() or argumentValues["region"].lower() == continent[0].lower():
                    regionFilter = f"AND Continents.ID = \"{continent[0]}\""
                    regionName = continent[2]
                    break

            if not regionFilter:
                countries = self.bot.db.executeQuery("SELECT Code, Name FROM Countries")
                for country in countries:
                    if argumentValues["region"].lower() == country[1].lower():
                        regionFilter = f"AND Countries.Code = \"{country[0]}\""
                        regionName = country[1].title()
                        break


            if not regionFilter:
                return "Invalid region!"
        
        if "includeExtensions" in argumentValues.keys():
            if argumentValues["includeExtensions"] == "true":
                includeExtensions = 1


        records = self.bot.db.executeQuery(f"""
        SELECT RunCategories.Category, MIN(Runs.Time), Users.Name
        FROM RunCategories 
        LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
        LEFT JOIN Users ON Runs.Runner = Users.ID
        LEFT JOIN Countries ON Users.Nationality = Countries.Code
        LEFT JOIN Continents ON Countries.Continent = Continents.ID
        LEFT JOIN Categories ON RunCategories.Category = Categories.ID
        WHERE Categories.Extension <= ?
        {regionFilter}
        GROUP BY RunCategories.Category
        """, (includeExtensions,))

        # Formatting :D
        header = f"{regionName} Records:"

        table = [["Category", "Time", "Runner"]]
        for record in records:
            table.append([record[0].title(), Helpers.durations.formatted(record[1]), record[2]])


        output = header+"\n```"
        output += Helpers.neatTables.generateTable(table)+"```"
        return output