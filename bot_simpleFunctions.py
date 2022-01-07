import discord
from discord.ext import tasks, commands
import asyncio
import datetime as dt
from datetime import datetime as datetime
from collections import deque
import random
import sys
import datetime as dt
from discord.ui import Button
from discord.ui import View


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("C H A D can say hi")
        # Ready message

    @commands.command(name='Hi', help='Biggest Brains function')
    async def Hi(self, ctx):
        button=Button(label="Hello", style=discord.ButtonStyle.link,url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",emoji="👋")
        view=View()
        view.add_item(button)
        await ctx.send("Hi fellow Chad.",view=view)
        return

    @commands.command(name='ping', help='returns ping\latency  AND pings u')
    async def ping(self, ctx):
        await ctx.reply('Pong! {0}'.format(round(self.bot.latency*100, 1)))
        return


def setup(bot):
    bot.add_cog(Basic(bot))
