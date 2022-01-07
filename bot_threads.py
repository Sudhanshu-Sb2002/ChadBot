import datetime as dt

import discord
from discord.ext import tasks, commands

threadtime = dt.timedelta(hours=23)

class Threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.threadlist=dict()
        print("C H A D can perform his thread duties")
        # Ready message

    @tasks.loop(seconds=threadtime.seconds)
    async def keep_threads_active(self):
        print(self.threadlist)
        for thread,yesno in self.threadlist.items():
            if yesno:
                await thread.send("Well, somebody's gotta keep the thread active")


    @commands.command(name='sot', help='Save our threads!!!')
    async def sot(self, ctx):
        server=ctx.guild
        for thread in server.threads:
            if not thread.archived and thread not in self.threadlist:

                self.threadlist[thread]=True
                await thread.join()

        self.keep_threads_active.start()
        return


    @commands.command(name='stopall', help='stop saving the threads')
    async def stopall(self, ctx):
        server=ctx.guild
        for thread in server.threads:
            if not thread.archived :

                self.threadlist[thread]=False
                await thread.join()


        return


    @commands.command(name='savethread', help='sends a message to this thread every 23 hrs')
    async def savethread(self, ctx):
        thread=ctx.channel
        if isinstance(thread,discord.threads.Thread) and not thread.archived:
            self.threadlist[thread] = True
            self.keep_threads_active.start()
            return

    @commands.command(name='dontsavethread', help='stops saving this thread from dying')
    async def dontsavethread(self, ctx):
        thread=ctx.channel
        if isinstance(thread,discord.threads.Thread) and not thread.archived:
            self.threadlist[thread] = False

            return


def setup(bot):
    bot.add_cog(Threads(bot))