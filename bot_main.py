import discord
from discord.ext import tasks, commands
import asyncio
import datetime as dt
from datetime import datetime as datetime
from collections import deque
import random
import sys
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

bot.run('ODA2MzM5MjA1Mjc3ODEwNjk4.YBn_5w.usdcqmgloVGo8Omtzv5jH9JNlgo', reconnect=True)

