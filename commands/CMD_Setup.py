import cobble.command
import cobble.validations
import discord

import cobble.permissions
import Database.User
import Database.Category
import Helpers.durations
import Helpers.neatTables

class SetupCommand(cobble.command.Command):
    def __init__(self, bot: cobble.bot.Bot):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, 
                         name="Setup",
                         trigger=["setup", "su"],
                         description="See your (or another person's) setup",
                         permission="default")
        
        self.addArgument(cobble.command.Argument(
            "player",
            "The name of the player",
            cobble.validations.IsString(),
            keywordArg=True
        ))
        
        
    async def execute(self, messageObject: discord.message.Message, argumentValues: dict, attachedFiles: dict) -> str:
        if "player" in argumentValues.keys():
            userID = Database.User.identifyUser(self.bot.db, username=argumentValues["player"])
            if userID == None:
                return "User not found!"
        else:
            userID = Database.User.identifyUser(self.bot.db, discordID=messageObject.author.id)
            if userID == None:
                return "No data for user. Please link your discord with your speedrun.com account using the `.iam` command"
            
        user = Database.User.User(self.bot.db, userID)
        result = self.bot.db.executeQuery("""
                                             SELECT SetupElement, SetupValue, SetupNum
                                             FROM UserSetups
                                             WHERE UserID = ?
                                             """, (userID,))
        if len(result) == 0:
            return "You have no recorded setup!"
        setupInfo = {x[0]: [x[1], x[2]] for x in result}

        output = f"{user.name}'s setup:\n```"
        tableData = []
        peripheralElements = ["keyboard", "mouse", "hz"]
        settingsElements = ["dpi", "sensitivity"]

        sections = [["Peripherals", peripheralElements], ["Settings", settingsElements]]

        for section in sections:
            if len(list(set(section[1]) & set(setupInfo.keys()))) > 0:
                tableData.append([section[0], ""])


            # Add each "peripheral" element to the table output, in alphabetical order
            for element in sorted(list(setupInfo.keys())):
                if element in section[1]:
                    # Crazy list comprehension extracts the value from the [value, None] or [None, value] structure
                    tableData.append([" "+str(element).capitalize(), str(next(item for item in setupInfo[element] if item is not None))])

            if section[0] == "Settings":
                if "dpi" in setupInfo.keys() and "sensitivity" in setupInfo.keys():
                    edpi = setupInfo["dpi"][1]*setupInfo["sensitivity"][1]
                    inchesper360 = round(360/(edpi*0.022), 1) # 0.022 is the default (and mandated) m_yaw value for portal
                    tableData.append([" eDpi", str(round(edpi, 1))])
                    tableData.append([" Inches/360", str(inchesper360)])
                    
        


        

        print(tableData)

        output += Helpers.neatTables.generateTable(tableData)+"```"



        return output


        
        
        

        