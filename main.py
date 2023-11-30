import cobble.bot
import cobble.command
import cobble.permissions
import os
import discord

import Database.Interface
dirPath = os.path.dirname(os.path.realpath(__file__))


database = Database.Interface.DatabaseInterface("Database/thatOtherLeaderboard.db")
tolBot = cobble.bot.Bot(dirPath+"/config.json", dirPath+"/cobble/permissions.json", "tolBot", ".", database)




tolBot.addCommand(cobble.command.HelpCommand(tolBot))
tolBot.addCommand(cobble.command.ListCommand(tolBot))

# Get the path of the commands directory
commandsDir = os.path.join(os.path.dirname(__file__), "commands")

# Iterate over the files in the commands directory
for filename in os.listdir(commandsDir):
    if filename.endswith(".py"):
        # Remove the file extension to get the command name
        commandName = filename[:-3]

        # Ensure it's labelled as a command
        if not commandName[:4] == "CMD_":
            continue
        
        # Import the command module dynamically
        module = __import__(f"commands.{commandName}", fromlist=[commandName])
        
        # Get the command class from the module
        commandClass = getattr(module, commandName[4:] + "Command")

        tolBot.addCommand(commandClass(tolBot))



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content:
        if message.content[0] == tolBot.prefix and message.content != tolBot.prefix*len(message.content):

            response, postCommand = await tolBot.processCommand(message, message.content[1:])
            if type(response) == str:
                await message.channel.send(response[:(min(len(response), 1999))])
            else:
                for part in response:
                    await message.channel.send(part)

            if postCommand:
                postCommand()




client.run(tolBot.token)