import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences=True
bot = commands.Bot(command_prefix=']', case_insensitive=True, intent=intents)

initial_extensions=['bot_simpleFunctions','bot_messageCounter',"bot_threads"]
def main():
    for extension in initial_extensions:
        bot.load_extension(extension)
if __name__ == '__main__':
    main()
    #extension=''
    #try:
        #for extension in initial_extensions:
            #bot.load_extension(extension)
    #except:
        #for extension in initial_extensions[initial_extensions.index(extension)+1]:
            #bot.load_extension(extension)
        #bot.load_extension()
@bot.event
async def on_ready():
    print(bot.guilds)
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="]help (cos this server dead)"))
    print(f'Successfully logged in and booted...!')

bot.run(TOKEN, reconnect=True)

